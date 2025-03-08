// Position Settings
TweenMax.set("#sun", {y:-100})
TweenMax.set("#Mountain-1", {x:-1181})
TweenMax.set("#back-trees-1", {x:-1618})
TweenMax.set("#middle-trees-1", {x:-1618})
TweenMax.set("#middle-trees-1, #middle-trees-2", {y:60})
TweenMax.set("#bird-container", {y:-80, x:250})
TweenMax.set(".bird-body", {scaleY:1.2})
TweenMax.set("#front-trees-1", {x:-1178})
TweenMax.set("#front-trees-1, #front-trees-2", {y:50})

// Animations

// Frame
TweenMax.fromTo("#window", 1, {y:-2}, {y:2, repeat:-1, yoyo:true, ease: Sine.easeInOut}, )

// Front Trees
TweenMax.to("#front-trees-1", 10, {x:-2356, ease:Linear.easeNone, repeat:-1})
TweenMax.to("#front-trees-2", 10, {x:-1178, ease:Linear.easeNone, repeat:-1})

// Middle Trees
TweenMax.to("#middle-trees-2", 25, {x:-1618, ease:Linear.easeNone, repeat:-1})
TweenMax.to("#middle-trees-1", 25, {x:-3235, ease:Linear.easeNone, repeat:-1})

// Back Trees
TweenMax.to("#back-trees-2", 45, {x:-1618, ease:Linear.easeNone, repeat:-1})
TweenMax.to("#back-trees-1", 45, {x:-3235, ease:Linear.easeNone, repeat:-1})

// Mountains
TweenMax.to("#Mountain-1", 60, {x:-2362, ease:Linear.easeNone, repeat:-1})
TweenMax.to("#Mountain-2", 60, {x:-1181, ease:Linear.easeNone, repeat:-1})

// Sun
TweenMax.to("#sun", 60, {y:300, x:10, ease:Linear.easeNone})

// Birds
TweenMax.to("#bird-container", 100, { x:-1000, ease:Linear.easeNone})


// Colors
TweenMax.to(".st0, .st20", 40, {fill:"hsl(-=50, -=10, -=7)", delay:25})
TweenMax.to(".st2", 40, {fill:"hsl(-=5, -=60, -=40)", delay:25})
TweenMax.to(".st3", 40, {fill:"hsl(-=50, -=20, -=30)", delay:25})
TweenMax.to(".st4", 40, {fill:"hsl(-=50, -=80, -=30)", delay:25})
TweenMax.to(".st5", 40, {fill:"hsl(+=0, -=30, -=20)", delay:25})
TweenMax.to(".st6", 40, {fill:"hsl(+=0, -=30, -=20)", delay:25})
TweenMax.to(".st20", 40, {fill:"hsl(+=0, -=10, -=20)", delay:25})
TweenMax.to(".st19", 50, {fill:"hsl(+=0, -=0, +=90)", delay:40})

// Bird Wings
flapWings()

function flapWings(){
  [
    "#wing-1",
    "#wing-2",
    "#wing-3",
    "#wing-4",
    "#wing-5",
    "#wing-6",
  ].forEach((wingId, index)=>
            {
    TweenMax.to(wingId, 1+ .1*index, {scaleY:-1.2, transformOrigin:"bottom center", yoyo:true, repeat:-1, ease: Sine.easeInOut})
  })
}