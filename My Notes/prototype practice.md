```javascript
function obj(name) {
    this.name = name;
    this.age = 26;
    obj.prototype.sayName = () => {
        console.log("obj.prototype.sayName " + this.name)
    }
    obj.prototype.sayHi = () => {
        console.log("hi1")
    }
}
obj.prototype = {
    type: 'Boolean',
    sayType() {
        console.log(this.age);
        console.log(obj.prototype.type)
    },
    sayHi() {
        console.log('hi2')
    }
}

var a = new obj("fyg");
console.log(a.prototype) //undefined 实例的 prototype 和构造函数的原型对象没有任何关系 
// 倒是 原型.__proto__ 指向构造函数的原型对象
a.prototype = {
    sayAge: () => {
        console.log(this.age)
    }
}
a.prototype.sayCode = function() {
    console.log(this.code);
}
a.prototype.sayHi = function() {
    console.log("hi3");
}
console.log(a.prototype) //这里给 a的 prototype 改写、增加了方法以后，就可以看到了
a.sayName();        
a.sayType()         //注意！！！ 这里可以访问到 26
//如果 obj.prototype 中的 sayType 换成

// sayType:()=>{} 因为封闭作用域，就访问不到啦！！！


a.sayHi();  // "hi1"  构造函数公有方法会屏蔽原型对象上的同名方法
```