# 1
## 1 遍历、获取DOM元素：
```js
function $$(selector, context) {
    context = context || document;
    var elements = context.querySelectorAll(selector);
    return Array.prototype.slice.call(elements);
}
```


## 2 一些回退机制
- 有厂商前缀的语法，保持标准语法在最后
- 指定一个渐变色作为背景时候，应该在前面添加一行实色背景的声明，这个实色背景最好取渐变色的平均色值
- Modernizr    ?
- @supports
- 或者，手动检测属性是否被支持，思路是在任一元素的element.style 对象上检查该属性是否存在：

```JS
function testProperty(property) {
	var root = document.documentElement;
	if (property in root.style) {
	root.classList.add(property.toLowerCase());
	return true;
	}
	root.classList.add('no-' + property.toLowerCase());
	return false;
}
```

但是这样子检测时候会改变元素样式，所以来一个 隐藏的元素检测：
```JS
function testValue(id, value, property) {
	var dummy = document.createElement('p');
	dummy.style[property] = value;
	if (dummy.style[property]) {
	root.classList.add(id);
	return true;
	}
	root.classList.add('no-' + id);
	return false;
}
```
## 3 一些技巧
* 当某些值相互依赖时，应该把它们的相互关系用代码表达出来
  比如：
  font-size: 20px;
  line-height: 30px;
  可以换成：
  font-size: 20px;
  line-height: 1.5;

* 易于维护和代码精简不可兼得
  比如一个
  border-width:10px 10px 10px 0;
  可以写成：
  border-width:10px;
  border-left-width:0;

* currentColor
  hr:{
  height: .5em;
  background:currentColor;
  }

* inherit 总是绑定到父元素的计算值
* 要给按钮实现 hover、click的明暗色调变化时，可以叠加一个半透明的黑色或者白色：
  `background: #58a linear-gradient(hsla(0,0%,100%,.2),transparent);`

* inherit 总是会绑定到父元素的计算值
* 合理简写，保持代码 DRY 如：
```CSS
background: url(tr.png) no-repeat top right / 2em 2em,
url(br.png) no-repeat bottom right / 2em 2em,
url(bl.png) no-repeat bottom left / 2em 2em;

可以写成
background: url(tr.png) top right,
url(br.png) bottom right,
url(bl.png) bottom left;
background-size: 2em 2em;
background-repeat: no-repeat;
```
> 列表扩散规则:如果只为某个属性提供一个值，那它就会扩散并应用到列表中的每一项

> `background: url(tr.png) no-repeat top right / 2em 2em,`
> `/` 是为了消除歧义，top right 是 background-position ，而 2em 2em 是
> background-size 加上斜杠防止 2em 被理解为background-position


## 4 响应式设计的一些最佳实践
- 使用百分比,或者和 视口相关的单位。（vw， vh，wmin， vmax）
- 需要在较大分辨率下得到固定宽度时，使用 max-width 而不是
  width ，因为它可以适应较小的分辨率，而无需使用媒体查询。
- 不要忘记为替换元素（比如 img 、 object 、 video 、 iframe 等）设
  置一个 max-width ，值为 100% 。
- 背景图片需要完整地铺满一个容器，不管容器的尺寸如何变化，
  `background-size: cover` 这个属性都可以做到
- 在使用多列文本时，指定` column-width` （列宽）而不是指定
  `column-count` （列数），这样它就可以在较小的屏幕上自动显示为单
  列布局。


# 2 background  border

## 1 translucent border
```
H：Hue(色调)。0(或360)表示红色，120表示绿色，240表示蓝色，也可取其他数值来指定颜色。取值为：0 - 360
S：Saturation(饱和度)。取值为：0.0% - 100.0%
L：Lightness(亮度)。取值为：0.0% - 100.0%
A：Alpha透明度。取值0~1之间。
```
设置透明边框时，因为默认情况下，背景会延伸到边框所在的区域下层，所以透明边框会和背景色叠加，得不到想要的透明色。

可以设置
```CSS
background-clip:padding-box;
```
来对背景裁切。





## 2 多重边框
### box-shadow
box-shadow 支持逗号分隔语法，可以创建任意数量的投影，来模拟边框的效果：

```css
background: yellowgreen;
box-shadow: 0 0 0 10px #655,
0 0 0 15px deeppink,
0 2px 5px 15px rgba(0,0,0,.6);
```
box-shadow 是层层叠加，所以第二道阴影应该是 10+5 px

Attention:
- 投影的行为跟边框不完全一致，因为它不会影响布局，而且也不会
  受到 box-sizing 属性的影响。但可以通过内边距或外边距来额外模拟出边框所需要占据的空间
- 假“边框”出现在元素的外圈不会响应鼠标事件，如果需要，可以给box-shadow 属性加上 inset 关键字，来使投影绘制在元素的内圈


### outline
只需要两层边框时，可以先设置一层常规边框，再加上 outline 属性来产生外层的边框。

outline 样式十分灵活，不像上面的 box-shadow 方案只能模拟实线边。

可以通过 outline-offset 属性来控制它跟元素边缘之间的间距

## 3 背景定位
可以在偏移量前面指定关键字，指定背景图片距离任意角的偏移量
如：
```CSS
background: url(code-pirate.svg) no-repeat #58a;
background-position: right 20px bottom 10px;
```

> 默认情况下， background-position 是以 padding box 为准的，这样边
> 框才不会遮住背景图片

但是这时候如果需要上面的值设定跟 padding 一样时，若对 padding 有任何修改，则需要一起修改 right、bottom后面的值。更 DRY 的方式如下：


当需要背景图片保持跟 padding 一样的偏移时，可以通过CSS3添加的 ` background-origin` 属性。

它的默认值是 ` padding-box ` ，若改成` content-box ` ，则背景图片会保持跟 padding 一样的缩进。


或者可以使用计算属性：
```CSS
background-position: calc(100% - 20px) calc(100% - 10px);
```
> calc(a - b) + - 计算符两边必须要有空格


## 4 边框内圆角

需要边框内圆角时，可以这样模拟：
```html
<div class="something-meaningful"><div>
I have a nice subtle inner rounding,
don't I look pretty?
</div></div>
<style>
.something-meaningful {
background: #655;
padding: .8em;
}
.something-meaningful > div {
background: tan;
border-radius: .8em;
padding: 1em;
}
</style>
```

更好的方式是只是用一个元素：
> outline 不会跟着圆角描绘，只会显示出直角。而 box-shadow 可以填补 outline 和 radius 之间的空隙，两者组合就可以做出边框内圆角。

> box-shadow 属性指定的扩张值并不一定等于描边的宽度，只需要指定一个足够填补“空隙”的扩张值就可以了。，指定一个等于描边宽度的扩张值在某些浏览器中可能会得到渲染异常，因此需要一个稍小些的值

```CSS
background: tan;
border-radius: .8em;
padding: 1em;
box-shadow: 0 0 0 .6em #655;
outline: .6em solid #655;
```

## 5 条纹背景
### 水平条纹
```CSS
background: linear-gradient(#fb3 50%, #58a 0);
background-size: 100% 30px;
```
> linear-gradient 中第二个色标的大小为 0 时，会被自动计算为 100% - 第一个色标大小，所以可以一直将第二个色标设为 0 。

### 竖直条纹
同水平条纹，不过指定方向，交换background-size
```CSS
background: linear-gradient(to right, /* 或 90deg */
#fb3 50%, #58a 0);
background-size: 30px 100%;
```


### 斜角条纹
```CSS
background: repeating-linear-gradient(45deg,
#fb3, #58a 30px);
```

当色标是同色系时，可以更 DRY：
```CSS
background: #58a;
background-image: repeating-linear-gradient(30deg,
hsla(0,0%,100%,.1),
hsla(0,0%,100%,.1) 15px,
transparent 0, transparent 30px);
```

## 6 复杂背景组合
### 网格
把多个渐变图案组合起来，让它们透过彼此的透明区域显现
```CSS
background: white;
background-image: linear-gradient(90deg,
rgba(200,0,0,.5) 50%, transparent 0),
linear-gradient(
rgba(200,0,0,.5) 50%, transparent 0);
background-size: 30px 30px;
```
也可以做成细线分隔的格子，即使用长度而不是百分比作为色标：
```CSS
background: #58a;
background-image:
linear-gradient(white 1px, transparent 0),
linear-gradient(90deg, white 1px, transparent 0);
background-size: 30px 30px;
```

更复杂的网格：
```CSS
background: #58a;
background-image: linear-gradient(white 2px, transparent 0),
                  linear-gradient(90deg, white 2px, transparent 0),
                  linear-gradient(hsla(0,0%,100%,.3) 1px, transparent 0),
                  linear-gradient(90deg, hsla(0,0%,100%,.3) 1px, transparent 0);
background-size: 50px 50px, 50px 50px,
                 10px 10px, 10px 10px;
```


### 波点
```CSS
background: #655;
background-image: radial-gradient(tan 30%, transparent 0);
background-size: 30px 30px;
```
更密集、漂亮的波点:
```CSS
background: #655;
background-image: radial-gradient(tan 30%, transparent 0),
radial-gradient(tan 30%, transparent 0);
background-size: 30px 30px;
background-position: 0 0, 15px 15px;
```
但是这样子代码修改量较大，参考 mixin：
```SCSS
@mixin polka($size, $dot, $base, $accent) {
background: $base;
background-image:
radial-gradient($accent $dot, transparent 0),
radial-gradient($accent $dot, transparent 0);
background-size: $size $size;
background-position: 0 0, $size/2 $size/2;
}
```
使用：`@include polka(30px, 30%, #655, tan);`

### 棋盘
```CSS
background: #eee;
background-image:
linear-gradient(45deg, #bbb 50%, transparent 0);
background-size: 30px 30px;
```
会得到三角形，再来一个倒三角形
`linear-gradient(45deg, transparent 75%, #bbb 0);`
两个组合：
```CSS
background: #eee;
background-image:
linear-gradient(45deg, #bbb 25%, transparent 0),
linear-gradient(45deg, transparent 75%, #bbb 0);
background-size: 30px 30px;
```
再加一半，组合到一起：

```CSS
background: #eee;
background-image:
linear-gradient(45deg, #bbb 25%, transparent 0),
linear-gradient(45deg, transparent 75%, #bbb 0),
linear-gradient(45deg, #bbb 25%, transparent 0),
linear-gradient(45deg, transparent 75%, #bbb 0);
background-position: 0 0, 15px 15px,
15px 15px, 30px 30px;
background-size: 30px 30px;
```

## 7 伪随机背景
> 让随机性更加真实，需要把贴片的尺寸最大化

> 为了让最小公倍数最大化，这些数字最好是“相对质数”

> 相对质数是数字之间的关系，而不是单个数字自身的属性。构成相对质数的这些数字没有公约数，但它们自己是可以有多个约数的（比如说，10 和 27 是相对质数，但它们都不是质数）。很显然，一个质数跟其他所有数字都可以构成相对质数。

```CSS
background: hsl(20, 40%, 90%);
background-image:
linear-gradient(90deg, #fb3 11px, transparent 0),
linear-gradient(90deg, #ab4 23px, transparent 0),
linear-gradient(90deg, #655 41px, transparent 0);
background-size: 41px 100%, 61px 100%, 83px 100%;
```


## 8 连续的图像边框

可以使用 `border-image` 切割图片，再将图片应用到边角。
```CSS
<repeating-linear-gradient> = linear-gradient([ [ <angle> | to <side-or-corner> ] ,]? <color-stop>[, <color-stop>]+)

<side-or-corner> = [left | right] || [top | bottom]

<color-stop> = <color> [ <length> | <percentage> ]?
```

例如一个 信封边框:
```CSS
padding: 1em;
border: 1em solid transparent;
background: linear-gradient(white, white) padding-box,
repeating-linear-gradient(
-45deg,
red 0,
red 12.5%,
transparent 0,
transparent 25%,
#58a 0,
#58a 37.5%,
transparent 0,
transparent 50%)
0 / 5em 5em;
```
也可以使用 `border-image` 实现：
```CSS
padding: 1em;
border: 16px solid transparent;
border-image: 16 repeating-linear-gradient(-45deg,
red 0, red 1em,
transparent 0, transparent 2em,
#58a 0, #58a 3em,
transparent 0, transparent 4em);
```




蚂蚁行军效果

```css
@keyframes ants { to { background-position: 100% } }
.marching-ants {
padding: 1em;
border: 1px solid transparent;
background:
linear-gradient(white, white) padding-box,
repeating-linear-gradient(-45deg,
black 0, black 25%, white 0, white 50%
) 0 / .6em .6em;
animation: ants 12s linear infinite;
}
```

```
# background 的简写
background-color
background-position：top top | x% y% | xpos ypos
background-size：length | percentage | cover | contain;
    cover:把背景图像扩展至足够大，以使背景图像完全覆盖背景区域。
    cotain：把图像图像扩展至最大尺寸，以使其宽度和高度完全适应内容区域。
background-repeat
background-origin：padding-box | border-box | content-box;
    规定背景图片的定位区域，背景图像相对于内边距框、边框盒、内容框来定位
background-clip：border-box | padding-box | content-box;
    规定背景的绘制区域，背景被裁剪到边框盒、内边距框、内容框。
background-attachment: scroll | fixed;
    页面的其余部分滚动时，背景图像不会移动
background-image
```

# 3 形状
## 1 自适应椭圆
对于圆角，如果指定任何大于 100px 的半径，仍然可以得到一个圆形
> 规范：当任意两个相邻圆角的半径之和超过 border box 的尺寸时，用户代理必须按比例减小各个边框半径所使用的值，直到它们不会相互重叠
> 为止。

`border-radius` 可以单独指定水平和垂直半径，只要用一个斜杠（ / ）分隔这两个值

使用百分比作为单位时，宽度用于水平半径的解析，而高度用于垂直半径的解析



# 8 过渡与动画
## 缓动效果

> 用 height 而不是变形属性来实现提示框的展示动画，可能会发现从 height: 0（或其他值）到 height: auto 的过渡并不会生效。这是因为 auto是一个关键字，无法解析为一个可动画的值。在这种场景下，可以改为对 max-height 属性进行过渡，并给这个属性指定一个足够大的值来作为展示状态。



缓动函数：除了内置，也可以用`cubic-bizier:(x1, y1, x2, y2)`自由指定两个锚点，参数值若超过1，则向反方向运动 



```css
input:not(:focus)+.callout {
      transform: scale(0);
      /* transition-timing-function: ease; */
      /* 如果没有上面这句， 当 blur 触发时，因为是同一个缓动函数 cubic-bezier(.25, .1, .3, 1.5) 所以会scale到 1.5去，所以最终消失掉时候还会放大，再消失，所以需要再加一个缓动函数覆盖掉他*/

      transition: .25s;
      /* 因为 blur 时候， 按上上面那句，是ease走的（transition默认的 animation-timing-function 就是 ease），持续时间 0.5s，但是之前focus时候没有按ease走了0.5秒，这里按ease走了0.5秒就感觉  blur 时候变慢了，所以需要修改一下 blur 时候的animation-duration,又因为同时需要修改 timing-function，所以用一个 transition 覆盖掉（默认会应用 ease）*/
    }

    .callout {
      transform-origin: 1.4em -.4em;
      transition: .5s cubic-bezier(.25, .1, .3, 1.5) transform;
      /* 防止颜色之类的属性被应用上 错误的 缓动函数，这里指定一下 transition-property 为 transform */
    }
    /*甚至可以通过transition-delay 属性把各个属性的过渡过程排成列队，这个属性的值实际上就是 transition简写属性中的第二个时间值。举例 来 说， 如 果 width 和 height都需要过渡效果，而且你希望高度先变化然后宽度再变化（很多弹出框脚本库已经把这种动画效果推广开来了），就可以这样写： transition: .5s height,.8s .5s width; （ 也 就 是 说，让 width 过渡的延时正好等于height 过渡的持续时间）。  */
```

```css
input:not(:focus) + .callout { transform: scale(0); }
.callout {
transform-origin: 1.4em -.4em;
transition: .5s cubic-bezier(.25,.1,.3,1.5);
}
```

还可以通过 transition-delay 属性把各个属性的过渡过程排成列队

```css
transition:  animation-name, animation-duration, animation-timing-function, animation-delay, animation-iteration-count, animation-direction animation-fill-mode
// 默认值
animation-name: none
animation-duration: 0s
animation-timing-function: ease
animation-delay: 0s
animation-iteration-count: 1
animation-direction: normal
animation-fill-mode: none
animation-play-state: running
```

所以，可以直接写成：
```css
transition: .5s height, .8s .5s width
```

## 逐帧动画
> 2004 年，Mozilla 发起了一个建议：在 PNG 格式中增加对逐帧动画的支持，就像 GIF 格式同时支持静态图像和动画一样。这种格式被称作 `APNG`

>基于贝塞尔曲线的调速函数都会在关键帧之间进行插值运算，从而产生平滑的过渡效果

> animation 的 steps() 会根据你指定的步进数量，把整个动画切分为多帧，而且整个动画会在帧与帧之间硬切，不会做任何插值处理

> steps() 还接受可选的第二个参数，其值可以是 start 或 end（默认值）。这个参数用于指定动画在每个循环周期的什么位置发生帧的切换动作


如，对一个 雪碧图的“转菊花”进度图做处理时，可以这样做：
```css
@keyframes loader {
to { background-position: -550px 0; }
}
.loader {
width: 66px; 
height: 66px;
background: url(img/loader.png) 0 0;
animation: loader 1s infinite steps(8);
/* 把文本隐藏起来 */
text-indent: 200%;
white-space: nowrap;
overflow: hidden;
}
```

## 闪烁
让文字闪烁，可以使用动画
```css
    @keyframes blink-smooth {
      to {
        color: transparent
      }
    }

    div1 {
      animation: 1s blink-smooth 3;
    }
```
上面的动画，颜色出现时候很突兀，而且动画一直处于加速中
>animation-direction 的唯一作用就是反转每一个循环周期（ reverse ），或第偶数个循环周期（ alternate ），或第奇数个循环周期 （ alternate-reverse ）。它的伟大之处在于，它会同时反转调整函数，从而产生更加逼真的动画效果

所以可以这样处理

```css
animation: .5s blink-smooth 6 alternate;
```

因为现在一次淡入淡出的过程是由两个循环周期组成的，所以将 动画循环的次数翻倍,将持续时间减半,而得到平滑的闪烁效果

当只要直接闪烁，不要过渡时，若使用 `step()`：

```css
animation: 1s blink 3 steps(1); 
```

但是这样子相当于 `steps(1, end)` ，它表示当前颜色与 `transparent` 之间的过渡会在一次步进中完成，于是颜色值的切换只会发生在动画周期的末尾, 总之, `step` **起始值贯穿于整个动画周期，而终止值只在动画结尾的无限短的时间点处出现**，step(2) 也一样，所以，需要调整动画的关键帧，让切换动作发生在 50% 处：

```css
    @keyframes blink {
      50% {
        color: transparent
      }
    }

    div3 {
      animation: 1s blink 3 steps(1);
      /* 或用step-end */
    }
```