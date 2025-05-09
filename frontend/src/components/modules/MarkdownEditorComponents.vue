<template>
  <div class="markdown-editor">
    <!-- Toolbar -->
    <div class="toolbar">
      <button @click="applyFormat('bold')" class="toolbar-btn" title="Bold"><strong>B</strong></button>
      <button @click="applyFormat('italic')" class="toolbar-btn" title="Italic"><em>I</em></button>
      <button @click="applyFormat('heading')" class="toolbar-btn" title="Heading">H</button>
      <button @click="applyFormat('quote')" class="toolbar-btn" title="Quote">"</button>
      <button @click="applyFormat('code')" class="toolbar-btn" title="Code">&lt;/&gt;</button>
      <button @click="applyFormat('link')" class="toolbar-btn" title="Link">🔗</button>
      <button @click="applyFormat('image')" class="toolbar-btn" title="Image">🖼️</button>
      <button @click="applyFormat('ul')" class="toolbar-btn" title="Unordered List">•</button>
      <button @click="applyFormat('ol')" class="toolbar-btn" title="Ordered List">1.</button>
    </div>
    <!-- Editor and Preview -->
    <div class="editor-preview">
      <textarea
        v-model="content"
        @input="updatePreview"
        class="editor"
        placeholder="请输入 Markdown..."
      ></textarea>
      <div
        class="preview"
        v-html="sanitizedHtml"
      ></div>
    </div>
  </div>
</template>

<script>
import { ref, computed, watch, defineComponent, nextTick } from 'vue';
import { marked } from 'marked';
import DOMPurify from 'dompurify';

export default defineComponent({
  name: 'MarkdownEditor',
  props: {
    modelValue: {
      type: String,
      default: ''
    }
  },
  emits: ['update:modelValue'],
  setup(props, { emit }) {
    const content = ref('');

    const renderedHtml = computed(() => {
      return marked.parse(content.value);
    });

    const sanitizedHtml = computed(() => {
      return DOMPurify.sanitize(renderedHtml.value);
    });

    watch(sanitizedHtml, (val) => {
      emit('update:modelValue', val);
    });

    function updatePreview() {}

    function applyFormat(type) {
      const textarea = document.querySelector('textarea');
      const start = textarea.selectionStart;
      const end = textarea.selectionEnd;
      const selected = content.value.slice(start, end);
      let insert;
      switch (type) {
        case 'bold':
          insert = `**${selected}**`;
          break;
        case 'italic':
          insert = `*${selected}*`;
          break;
        case 'heading':
          insert = `# ${selected}`;
          break;
        case 'quote':
          insert = `> ${selected}`;
          break;
        case 'code':
          insert = `\`${selected}\``;
          break;
        case 'link':
          insert = `[${selected || 'link text'}](url)`;
          break;
        case 'image':
          insert = `![${selected || 'alt text'}](image-url)`;
          break;
        case 'ul':
          insert = selected
            .split('\n')
            .map(line => `- ${line}`)
            .join('\n');
          break;
        case 'ol':
          insert = selected
            .split('\n')
            .map((line, i) => `${i + 1}. ${line}`)
            .join('\n');
          break;
      }
      content.value =
        content.value.slice(0, start) + insert + content.value.slice(end);
      nextTick(() => {
        textarea.setSelectionRange(start, start + insert.length);
        textarea.focus();
      });
    }

    return {
      content,
      sanitizedHtml,
      applyFormat,
      updatePreview
    };
  }
});
</script>

<style scoped>
.markdown-editor {
  display: flex;
  flex-direction: column;
  border: 1px solid #d1d5db;
  border-radius: 10px;
  overflow: hidden;
  font-family: 'Segoe UI', sans-serif;
  background-color: #ffffff;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
}

.toolbar {
  display: flex;
  flex-wrap: wrap;
  background-color: #f9fafb;
  padding: 0.5rem;
  border-bottom: 1px solid #e5e7eb;
}

.toolbar-btn {
  margin: 0.25rem;
  padding: 0.4rem 0.6rem;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  background-color: #f3f4f6;
  cursor: pointer;
  font-size: 14px;
  transition: 0.2s;
  min-width: 32px;
  text-align: center;
}

.toolbar-btn:hover {
  background-color: #e5e7eb;
  border-color: #9ca3af;
}

.editor-preview {
  display: flex;
  height: 500px;
}

.editor {
  flex: 1;
  padding: 1rem;
  border: none;
  border-right: 1px solid #e5e7eb;
  resize: none;
  font-family: monospace;
  font-size: 14px;
  outline: none;
}

.preview {
  flex: 1;
  padding: 1rem;
  overflow-y: auto;
  background-color: #f9fafb;
  color: #111827;
}
</style>