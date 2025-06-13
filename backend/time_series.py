'''
- 文件描述：明康慧医MKTY智慧医疗系统 融合文本的医学时间序列预测模型 模型原型建模代码
- 总负责人：齐鲁工业大学（山东省科学院）计算机科学与技术学部 软件工程（软件开发）21-1班 杜宇 (@duyu09, <202103180009@stu.qlu.edu.cn>)
- 文件名：time_series.py
- 著作权声明：Copyright (c) 2025 DuYu (https://github.com/duyu09/MKTY-System)
'''

import os
import torch
import torch.optim as optim
from torch import nn
from torch.utils.data import Dataset, DataLoader
from tqdm import tqdm

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class CrossAttention(nn.Module):
    def __init__(self, text_dim, freq_dim):
        super().__init__()
        self.query = nn.Linear(freq_dim, freq_dim)  # 频域作为Query
        self.key = nn.Linear(text_dim, freq_dim)  # 文本作为Key
        self.value = nn.Linear(text_dim, freq_dim)  # 文本作为Value

    def forward(self, freq, text):
        Q = self.query(freq)  # (batch, freq_dim)
        K = self.key(text)  # (batch, freq_dim)
        V = self.value(text)  # (batch, freq_dim)

        attn_weights = torch.softmax(Q * K, dim=-1)  # 点积注意力
        output = attn_weights * V  # (batch, freq_dim)
        return output


class MktyTimeSeriesPredictor(nn.Module):
    def __init__(self, input_dim=64, output_dim=16, text_dim=1024, text_aim_dim=128, hidden_size=128, num_layers=2):
        super().__init__()
        self.cross_attention = CrossAttention(text_aim_dim, input_dim)
        self.text_proj = nn.Sequential(
            nn.Linear(text_dim, 256),
            nn.LeakyReLU(),
            nn.Linear(256, text_aim_dim)
        )
        self.gate = nn.Sequential(
            nn.Linear(input_dim, 128),
            nn.LeakyReLU(),
            nn.Linear(128, input_dim)
        )
        self.lstm = nn.LSTM(1, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Sequential(nn.Linear(hidden_size, hidden_size),
                                nn.LeakyReLU(),
                                nn.Linear(hidden_size, 1))
        self.input_dim = input_dim
        self.output_dim = output_dim

    def forward(self, data, text_feature, use_text_enhance=True):  # data的长度须为偶数
        # assert data.shape[1] % 2 == 0, "data 必须是偶数"
        x = data.unsqueeze(-1)
        outputs = []
        hidden = None
        out, hidden = self.lstm(x, hidden)  # 先通过已有序列初始化隐藏状态
        input_t = x[:, -1:, :]  # 取最后一个时间步作为未来输入起点
        for _ in range(self.output_dim):
            out, hidden = self.lstm(input_t, hidden)  # 单步推进 LSTM
            pred = self.fc(out)  # shape: (batch, 1, 1)
            outputs.append(pred)
            input_t = pred  # 自回归输入
        result_data = torch.cat(outputs, dim=1)  # shape: (batch, pred_len, 1)
        result_data = result_data.squeeze(-1)
        if use_text_enhance:
            fft_result = self.fft_transform(data)
            dc, data_feature = fft_result[:, :1], fft_result[:, 1:]
            text_feature = self.text_proj(text_feature)
            adjusted_data_feature = self.cross_attention(data_feature, text_feature)
            gate_vector = torch.sigmoid(self.gate(adjusted_data_feature))
            adjusted_data_feature = torch.cat([torch.zeros_like(dc), adjusted_data_feature], dim=1)  # DC置零
            adjusted_result_data = self.inverse_fft_transform(adjusted_data_feature)
            gate_vector = gate_vector[:, :self.output_dim]
            adjusted_result_data = adjusted_result_data[:, :self.output_dim]
            result_data = gate_vector * result_data + (1 - gate_vector) * adjusted_result_data
        return result_data

    @staticmethod
    def fft_transform(x):
        """
        输入: (batch_size, x), x为偶数
        输出: (batch_size, x+1), 格式为 [DC振幅, 频率1振幅, ..., 频率N振幅, 频率1相位, ..., 频率N相位]
        """
        assert x.shape[1] % 2 == 0, "x 必须是偶数"

        # 计算 FFT (输出复数张量, 形状 (batch_size, x))
        X = torch.fft.rfft(x)  # 使用 rfft 仅计算非负频率 (输出长度: x//2 + 1)

        # 提取振幅和相位
        amplitude = torch.abs(X)  # (batch_size, x//2 + 1)
        phase = torch.angle(X)  # (batch_size, x//2 + 1)

        # 拼接结果 [DC振幅, 频率1振幅, ..., 频率N振幅, 频率1相位, ..., 频率N相位]
        # 注意: 相位部分跳过 DC（DC相位无意义，通常为0）
        result = torch.cat([
            amplitude,  # 所有振幅
            phase[:, 1:],  # 跳过 DC 相位
        ], dim=1)

        return result

    @staticmethod
    def inverse_fft_transform(fft_result):
        """
        输入:
            fft_result: (batch_size, x+1), 格式为 [DC振幅, 频率1振幅, ..., 频率N振幅, 频率1相位, ..., 频率N相位]
            original_x_length: 原始信号长度 x（偶数）
        输出: 重建的原始信号 (batch_size, x)
        """
        batch_size = fft_result.shape[0]
        original_x_length = fft_result.shape[1] - 1  # 原始信号长度
        n_freq = original_x_length // 2  # 正频率数量（不含DC）

        # 分离振幅和相位
        amplitude = fft_result[:, :n_freq + 1]  # DC + 正频率振幅
        phase = fft_result[:, n_freq + 1:]  # 正频率相位

        # 构建复数频谱 (rfft 格式: 长度 x//2 + 1)
        # DC 相位设为0，其他频率相位取自输入
        X_real = amplitude * torch.cos(torch.cat([
            torch.zeros(batch_size, 1, device=fft_result.device),  # DC相位=0
            phase
        ], dim=1))
        X_imag = amplitude * torch.sin(torch.cat([
            torch.zeros(batch_size, 1, device=fft_result.device),  # DC相位=0
            phase
        ], dim=1))
        X = torch.complex(X_real, X_imag)

        # 逆 FFT 恢复信号
        x_reconstructed = torch.fft.irfft(X, n=original_x_length)
        return x_reconstructed


class TimeSeriesDataset(Dataset):
    def __init__(self, data_list):
        """
        初始化数据集
        :param data_list: 大列表，每个元素是子列表[b_tensor, a_tensor, c_tensor]
        """
        self.data = data_list

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        b_tensor, a_tensor, c_tensor = self.data[idx]
        return b_tensor, a_tensor, c_tensor


# 数据加载函数
def load_data(pt_file_path):
    """
    从pt文件加载数据并创建数据集和数据加载器
    :param pt_file_path: pt文件路径
    :return: 训练数据加载器, 验证数据加载器
    """
    # 加载pt文件中的数据
    data_list = torch.load(pt_file_path)

    # 数据集划分比例
    train_ratio = 0.875
    train_size = int(train_ratio * len(data_list))
    val_size = len(data_list) - train_size

    # 划分训练集和验证集
    train_data, val_data = torch.utils.data.random_split(
        data_list, [train_size, val_size]
    )

    # 创建数据集
    train_dataset = TimeSeriesDataset(train_data)
    val_dataset = TimeSeriesDataset(val_data)

    # 创建数据加载器
    batch_size = 256  # 可根据需要调整
    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        collate_fn=lambda batch: tuple(torch.stack(samples) for samples in zip(*batch)))

    val_loader = DataLoader(
        val_dataset,
        batch_size=batch_size,
        shuffle=False,
        collate_fn=lambda batch: tuple(torch.stack(samples) for samples in zip(*batch)))

    return train_loader, val_loader


def train_model(model, train_loader, val_loader, epochs, learning_rate, save_model_path=None, lr_scheduler_step_size=45, lr_scheduler_gamma=0.1, use_text_enhance=True):
    """
    训练模型
    :param model: 要训练的模型
    :param train_loader: 训练数据加载器
    :param val_loader: 验证数据加载器
    :param epochs: 训练轮数
    :param learning_rate: 学习率
    """
    model = model.to(device)
    # criterion = nn.SmoothL1Loss(beta=1.0)
    # criterion = nn.L1Loss()
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=lr_scheduler_step_size, gamma=lr_scheduler_gamma)

    best_val_loss = 10000.0
    for epoch in range(epochs):
        model.train()  # 训练阶段
        train_loss = 0.0
        for b_batch, a_batch, c_batch in tqdm(train_loader, desc=f"Epoch {epoch + 1}/{epochs} - Training"):
            b_batch = b_batch.to(dtype=torch.float32).to(device)
            a_batch = a_batch.to(dtype=torch.float32).to(device)
            c_batch = c_batch.to(dtype=torch.float32).to(device)
            optimizer.zero_grad()
            pred = model(a_batch, b_batch, use_text_enhance=use_text_enhance)  # 前向传播
            loss = criterion(pred, c_batch)  # 计算损失
            loss.backward()  # 反向传播
            # torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=2.0)  # 梯度裁剪
            optimizer.step()
            train_loss += loss.item() * b_batch.size(0)
        train_loss = train_loss / len(train_loader.dataset)  # 计算平均训练损失
        scheduler.step()

        model.eval()  # 验证阶段
        val_loss = 0.0
        with torch.no_grad():
            for b_batch, a_batch, c_batch in tqdm(val_loader, desc=f"Epoch {epoch + 1}/{epochs} - Validation"):
                b_batch = b_batch.to(dtype=torch.float32).to(device)
                a_batch = a_batch.to(dtype=torch.float32).to(device)
                c_batch = c_batch.to(dtype=torch.float32).to(device)
                optimizer.zero_grad()
                pred = model(a_batch, b_batch, use_text_enhance=use_text_enhance)
                loss = criterion(pred, c_batch)
                val_loss += loss.item() * b_batch.size(0)
        val_loss = val_loss / len(val_loader.dataset)
        print(f"Epoch {epoch + 1}/{epochs} - Train Loss: {train_loss:.6f}, Val Loss: {val_loss:.6f}")  # 打印训练信息
        if (val_loss < best_val_loss) and save_model_path is not None:  # 保存最佳模型，模型名称为空则不保存。
            best_val_loss = val_loss
            torch.save(model.state_dict(), save_model_path)
            print("Saved best model!")
    print("Training complete!")
    return model


def kaiming_init_weights(m):  # 使用 Kaiming 初始化
    if isinstance(m, nn.Linear):
        nn.init.kaiming_normal_(m.weight, mode='fan_in', nonlinearity='leaky_relu')
        m.bias.data.fill_(0.0025)


def train_main(data_file_path, epochs, learning_rate, save_model_path, additional_train_model_path=None, use_text_enhance=True):
    print("Loading data...")
    train_loader, val_loader = load_data(data_file_path)
    model = MktyTimeSeriesPredictor()
    if additional_train_model_path:
        # 如果有额外的训练模型路径，则加载该模型
        model.load_state_dict(torch.load(additional_train_model_path))
        print(f"Loaded additional training model from {additional_train_model_path}")
    else:
        # 使用 Kaiming 初始化权重
        model.apply(kaiming_init_weights)

    train_model(
        model=model,
        train_loader=train_loader,
        val_loader=val_loader,
        epochs=epochs,
        learning_rate=learning_rate,
        save_model_path=save_model_path,
        use_text_enhance=use_text_enhance
    )


def inference(model_path, data_file_path, use_text_enhance=True):
    print("Loading data...")
    data = torch.load(data_file_path)
    data_s = data[3]
    b_batch, a_batch, c_batch = (data_s[0].unsqueeze(0).to(torch.float32).to(device),
                                 data_s[1].unsqueeze(0).to(torch.float32).to(device),
                                 data_s[2].unsqueeze(0).to(torch.float32).to(device))
    model = MktyTimeSeriesPredictor()
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.eval()

    with torch.no_grad():
        pred = model(a_batch, b_batch, use_text_enhance=use_text_enhance)

    import matplotlib.pyplot as plt
    plt.figure(figsize=(10, 5))
    pred = pred.cpu().numpy()
    c = c_batch.cpu().numpy()
    plt.plot(pred[0], label='Prediction')
    plt.plot(c[0], label='True Value')
    plt.title("1D Tensor Visualization - Line Plot")
    plt.xlabel("Index")
    plt.ylabel("Value")
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    # train_main(data_file_path=r"./data_new05.pt",
    #            epochs=175,
    #            learning_rate=4e-4,
    #            save_model_path=r"./model_new05_01.pth",
    #            additional_train_model_path=None,
    #            use_text_enhance=False
    #            )

    inference(model_path=r"./model_new05_01.pth",
              data_file_path=r"./data_new05_small.pt",
              use_text_enhance=False
              )
