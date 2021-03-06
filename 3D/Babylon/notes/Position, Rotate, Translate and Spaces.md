# rotation 和 position
## rotation
`pilot.rotation = new BABYLON.Vector3(alpha, beta, gamma)`

this is equivalent to

```
pilot.rotation.x  =  alpha;
pilot.rotation.y  =  beta;
pilot.rotation.z  =  gamma;
```
## 旋转轴

> The first thing to note is that the rotation takes place about axes local to the pilot. From the point of view of a simulation of the real world this makes sense, since when we observe things rotating generally we see them turning about their own local axes. For example watching a big (ferris) wheel or straightening a picture.

首先需要注意的是旋转发生时候的轴。从这点来看模拟真实世界是很有意义的，从我们观察事物的时候通常我们看到的是它旋转以它自己为中心的轴，比如看一个摩天轮的旋转。

如
```JS
pilot.rotation = new new BABYLON.Vector3(0, Math.PI/2, 0);
pilot.rotation = new new BABYLON.Vector3(Math.PI/2, 0, 0);
```

## position
> Just as pilot.position sets a position vector based from the world origin (0, 0, 0) so pilot.rotation sets, say, an 'orientation vector' starting from a local orientation matching the world orientation of (0, 0, 0). It is the last set rotation that is achieved.


和 `.position` 设置一个位置一样，每次会基于世界原点`(0，0，0)`开始移动，旋转也会这样子设置。即，一个 `方向向量`从局部方向开始匹配世界方向的`(0, 0, 0)`，即 从最初的状态开始旋转，所以每次会覆盖上次的旋转。

```
	pilot.rotation.y = Math.PI/2;
	pilot.rotation.x = Math.PI/2;
// x y 这两条操作，不会等于	
	pilot.rotation = new BABYLON.Vector3(Math.PI / 2, 0, 0);
	pilot.rotation = new BABYLON.Vector3(0, Math.PI / 2, 0);
	
// 而会合并到一条 pilot.rotation = new BABYLON.Vector3() 里面去
//  即 等于
pilot.rotation = new BABYLON.Vector3(Math.PI / 2, Math.PI / 2, 0);
```
http://www.babylonjs-playground.com/#UMR7M#11


### setPositionWithLocalVector
http://doc.babylonjs.com/features/position,_rotation,_scaling#align-axes

`mesh.setPositionWithLocalVector(new BABYLON.Vector3(x, y, z));`

获取 `LOCAL` 坐标的位置：
`var localPosition = mesh.getPositionExpressedInLocalSpace();`




# translate 和 rorate
## translate
http://www.babylonjs-playground.com/#UMR7M#14

`pilot.translate(vector, distance, space)` 
如
```JS
var distance = 1;
pilot.translate(new BABYLON.Vector3(3, 3, 3), distance, BABYLON.Space.WORLD);
```

space ：`BABYLON.Space.WORLD` | `BABYLON.Space.LOCAL`


`translate` 会根据上一个轴坐标位置进行移动


```JS
var distance = 1;
pilot.translate(new BABYLON.Vector3(3, 3, 3), distance, BABYLON.Space.WORLD);
```

移动的距离是 distance * 矢量坐标长度

即，原来位置 朝这个坐标的方向  移动  distance 个长度

比如 原来在 0,0,0 原点，那么 `translate(new BABYLON.Vector3(0, 1, 0), 1, BABYLON.Space.WORLD);` 就是像向 上 （y=1） 移动 1 个单位， 
`translate(new BABYLON.Vector3(0, 1, 0), 2, BABYLON.Space.WORLD);`
就是向上移动2个单位 这样子



或者给定一个`new BABYLON.Vector3(x, y, z)`向量组进行更精确的移动：

可用的常量：BABYLON.Axis.X  BABYLON.Axis.Y and BABYLON.Axis.Z

https://www.babylonjs-playground.com/#UMR7M#14

###  translate 的 Local Space 和 World Space
`BABYLON.Space.LOCAL` 和 `BABYLON.Space.WORLD`
> In the local space translate behaves as would a mathematical translate. That is, a sequence of translations is an accumulation of direction vectors as opposed to the setting of a position vector.

对于 translate 源码:
```js
public translate(axis: Vector3, distance: number, space?: Space): AbstractMesh {
    var displacementVector = axis.scale(distance);
    if (!space || (space as any) === Space.LOCAL) {
        var tempV3 = this.getPositionExpressedInLocalSpace().add(displacementVector);
        this.setPositionWithLocalVector(tempV3);
    }
    else {
        this.setAbsolutePosition(this.getAbsolutePosition().add(displacementVector));
    }
    return this;
}
```
**`translate` 在移动时候，`BABYLON.Space.LOCAL` 会每次根据自身坐标轴移动叠加**

**`BABYLON.Space.WORLD`每次会用自身当前位置，根据世界坐标轴移动**

【**`BABYLON.Space.WORLD`每次会用世界坐标加上自身坐标移动**】

> 如 translation (3, 3, 3) followed translation (2, 4, 1) results in the translation (5, 7, 4).

根据世界轴的 `translate` 和 position 表现一致


## rotate
**绕哪个轴旋转，即 去掉这个轴另外两个轴组成的面 绕这个轴来转动，比如，绕 y 轴转动，即 x-z 面绕 y轴转动**

`rotate(axis, amount, space) → AbstractMesh`
如
```JS
pilot.rotate(BABYLON.Axis.Y, Math.PI / 2, BABYLON.Space.WORLD);

```
- **根据世界轴旋转时，自身轴跟着物体本身旋转，自身轴最终将变为最后一次绕世界轴旋转后的状态**。
- **根据自身轴旋转时，每次旋转都是根据最新的自身轴旋转。因为自身轴跟着物体旋转，每转一次，自身轴所有的方向都变了，下一次旋转时候会继续根据新方向旋转**

> local-axes means axes local to the pilot that maintain their original orientation to the pilot, ie as the pilot turns the local axes turn with it.

> world-local-axes means axes local to the pilot that stay in the direction of the world axes whatever the orientation of the pilot.


### BABYLON.Space.WORLD
旋转会累积
 http://www.babylonjs-playground.com/#UMR7M#20

### BABYLON.Space.LOCAL
 http://www.babylonjs-playground.com/#UMR7M#36
 
 
 # 旋转轴想变就变！
 ```js
 mesh.setPivotPoint(new BABYLON.Vector3(-50, -50, 0))
 ```

`setPivotPoint` 默认是以 `LOCAL` 坐标旋转，也可以设为 `WORLD`

### rotationQuaternion
http://doc.babylonjs.com/features/position,_rotation,_scaling#align-axes
`rotationQuaternion` 通过围绕给定轴的旋转设置一个网格的取向。它是（x，y，z，w）的四维向量

```js
var axis = new BABYLON.Vector3(1, 1, 1);
var angle = Math.PI / 8;
var quaternion = new BABYLON.Quaternion.RotationAxis(axis, angle);
mesh.rotationQuaternion = quaternion;
```

#### Quaternion

http://doc.babylonjs.com/resources/rotation_conventions#quaternions

### RotationFromAxis
http://doc.babylonjs.com/features/position,_rotation,_scaling#align-axes
想要旋转摄像机或网格以使其与一组给定轴对齐时，使用 `RotationFromAxis` 方法查找要用于旋转的所需欧拉角度
```js
var orientation = BABYLON.Vector3.RotationFromAxis(axis1, axis2, axis3);
mesh.rotation = orientation;
```
其中轴1，的axis2和axis3三种左手正交向量和网孔将对准

- axis1作为本地系统中的x轴
- axis2作为本地系统中的y轴
- axis3作为本地系统中的z轴


## TransformNode
`TransformNode` 是一个未渲染的对象，但可以用作旋转中心（实际上是任何变换的中心）。可以减少内存使用并提高渲染速度。

```js
var pivot = new BABYLON.TransformNode("root");
pivot.position = CoR_At;

pilot.parent = pivot;
pilot.position = pilotStart;

pivot.rotate(axis, angle, BABYLON.Space.WORLD);
```

http://doc.babylonjs.com/how_to/pivot


## addRotation
http://doc.babylonjs.com/how_to/rotate

