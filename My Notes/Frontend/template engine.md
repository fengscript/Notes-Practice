```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta http-equiv="X-UA-Compatible" content="ie=edge" />
    <title>Document</title>
  </head>
  <body>
    <script type="template">
      {{each n in list}}
      <li>{{n}}</li>
      {{end}}
    </script>
    <script>
      let template = document.getElementById("template").innerText;
      function render(data) {
        let tempStr = "let str='';";
        const regexp = /\{\{.+\}\}/g;
        const beforeReg = /\w\s+(?=in)/;
        const afterReg = /(?<=\bin\b\s)\w+/;

        const getArray = match => match.match(afterReg)[0];
        const getItem = match => match.match(beforeReg)[0];
        let item = "";
        template = tempStr + template;
        template = template.replace(regexp, function(match) {
          if (match.indexOf("in") > -1) {
            tempStr = `${getArray(match)}.forEach(${getItem(
              match
            )}=> {str +=\``;
            item = getItem(match);
          }

          if (match.indexOf("end") > -1) {
            tempStr = "`});return str;";
          }

          if (new RegExp("{{\\s*" + item + "\\s*}}", "g").test(match)) {
            tempStr = "${" + item + "}";
          }
          return tempStr;
        });
        return new Function("list", template)(data);
      }

      document.getElementById("app").innerHTML = render([1, 2, 3]);
      /**
       * our target
       */
      // const temp =
      //   'let str = "";list.forEach(n => {str+=`<li>${n}</li>`});return str';
      // const t = new Function("list", temp);
      // console.log(t(test));

      /**
       *hard code version
       */
      //        let template = document.getElementById("template").innerText;
      // function render(data) {
      //   let tempStr = "let str='';";
      //   const regexp = /\{\{.+\}\}/g;
      //   const t = template.replace(regexp, function(match) {
      //     let temp = "";
      //     if (match.indexOf("in") > -1) {
      //       temp = `list.forEach( n => {str +=\``;
      //     }

      //     if (match.indexOf("end") > -1) {
      //       temp = "`});return str;";
      //     }

      //     if (match.indexOf("{{ n }}") > -1) {
      //       temp = "${n}";
      //     }
      //     return temp;
      //   });
      //   console.log(t);
      //   console.log(tempStr + t);
      //   return new Function("list", tempStr + t)(data);
      // }

      // document.getElementById("app").innerHTML = render([1, 2, 3]);
    </script>
  </body>
</html>
```