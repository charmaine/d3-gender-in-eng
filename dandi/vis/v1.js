// read in data and call visualize
$(function() {
  d3.csv("asee-profiles-2018.csv").then(function(data) {
    // values in every row
    let vals = Object.keys(data[0]);

    // group data by school
    var groups = _.groupBy(data, "Name");

    // group data in schools by level (Grad v Undergrad)
    for (i in groups) {
      var l = _.groupBy(groups[i], "Level");

      // group data in levels by department
      for (k in l) {
        var m = _.groupBy(l[k], "Department");

        for (j in m) {
          m[j] = _.map(m[j], function (d) {
            return d;
          });

          // combine all totals to find the total for a level/dept
          let comb = {};
          for (let i = 4; i < vals.length; i++) {
            comb[vals[i]] = m[j].reduce(function(prev, cur) {
              return prev + parseInt(cur[vals[i]], 10);
            }, 0);
          }

          m[j] = {
            byYear: m[j],
            combined: comb,
            department: j
          };
        }

        m = _.map(m, function (d) {
          return d;
        });

        m = m.sort(function(a, b) {
          if (a.combined["Total"] > b.combined["Total"]) {
            return 1;
          } else if (a.combined["Total"] < b.combined["Total"]) {
            return -1;
          } else {
            return 0;
          }
        });

        l[k] = {
          data: m,
          level: k
        };

        // remove departments with combined total of 0
        l[k].data = l[k].data.filter(function(d) {
          return d.combined["Total"] > 0;
        });
      }

      l = _.map(l, function (d) {
        return d;
      });

      groups[i] = {
        data: l,
        name: i
      };
    }

    groups = _.map(groups, function (d) {
      return d;
    });

    visualize(groups);
  })
})

var visualize = function(data) {
  // boilerplate setup
  var margin = { top: 50, right: 150, bottom: 50, left: 150 },
     width = 1080 - margin.left - margin.right,
     height = 360 - margin.top - margin.bottom;

  var svg = d3.select('#chart')
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .style("width", width + margin.left + margin.right + 500)
    .style("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  // log data for debuging
  console.log(data[109]);

  // colors
  var blue = "#5BC3EB";
  var pink = "#DE369D";
  var yellow = "#FED766";

  // display each school down the page
  // var schools = svg.selectAll(".school")
  //   .data(data)
  //   .enter().append("g")
  //   .attr("class", "school")
  //   .attr("transform", function(d, i) {
  //     return "translate(0, " + (i * 100) + ")";
  //   });

  // school text
  // schools.append("text")
  //   .text(function(d) {
  //     return d.name;
  //   });

  // I'm going to try making a bar chart for just one school bc why not
  // determine if school has the undergrad level
  let undergradIndex = data[109].data.map(function(e) { return e.level; }).indexOf("Undergrad");

  if (undergradIndex != -1) { // only render level if it exists
    // find largest total of gender categories
    let largestUM = Math.max.apply(Math, data[109].data[undergradIndex].data.map(a => a.combined["Total M"]));
    let largestUF = Math.max.apply(Math, data[109].data[undergradIndex].data.map(a => a.combined["Total F"]));
    let largestUO = Math.max.apply(Math, data[109].data[undergradIndex].data.map(a => a.combined["Total O"]));

    // find scale maximum
    let undergradScale = ((largestUM > (largestUF + largestUO)) ? largestUM : (largestUF + largestUO));

    var x = d3.scaleLinear()
      .range([0, (width / 2)])
      .domain([0, undergradScale]);

    var reversex = d3.scaleLinear()
      .range([0, (width / 2)])
      .domain([undergradScale, 0]);

    var y = d3.scaleBand()
      .range([margin.top, 238])
      .domain(data[109].data[undergradIndex].data.map(function(d) {
        return d.department;
      }))
      .padding(0.2);

    // y axis
    // TODO: make sure text doesn't overflow??
    svg.append("g")
      .attr("class", "yaxis")
      .attr("transform", "translate(" + (margin.left - 5) + ", 0)")
      .call(d3.axisLeft(y).tickSize(0))
      .style("text-transform", "uppercase")
      .style("font-size", "8px");

    // left side x axis
    svg.append("g")
      .attr("class", "xaxis")
      .attr("transform", "translate(" + margin.left + "," + (238 + 3) + ")")
      .style("font-size", "8px")
      .call(d3.axisBottom(reversex).tickSize(3).tickValues([undergradScale, 0]));

    // right side x axis
    // TODO: why is the end of the axis getting cut off
    svg.append("g")
      .attr("class", "xaxis")
      .attr("transform", "translate(" + (margin.left + (width / 2) + 5) + "," + (238 + 3) + ")")
      .style("font-size", "8px")
      .call(d3.axisBottom(x).tickSize(3).tickValues([0, undergradScale]));

    // left side bars
    svg.selectAll(".mbar")
      .data(data[109].data[undergradIndex].data)
      .enter().append("rect")
      .attr("class", "bar")
      .attr("x", function(d) {
        return (margin.left + (width / 2)) - x(d.combined["Total M"]);
      })
      .attr("y", function(d) {
        return y(d.department);
      })
      .attr("height", y.bandwidth())
      .attr("width", function(d) {
        return x(d.combined["Total M"]);
      })
      .attr("fill", blue);

    // right side bars
    svg.selectAll(".fbar")
      .data(data[109].data[undergradIndex].data)
      .enter().append("rect")
      .attr("class", "bar")
      .attr("x", margin.left + (width / 2) + 5)
      .attr("y", function(d) {
        return y(d.department);
      })
      .attr("height", y.bandwidth())
      .attr("width", function(d) {
        return x(d.combined["Total F"]);
      })
      .attr("fill", pink);

      // TODO: add 'other' bar at the end of fbar
  }

  var searchData = [];
   for (let i = 0; i < data.length; i++) {
     searchData.push(data[i].name);
   }

   var findNode = function(node, id) {
     if (node.data.id == id) {
       return node;
     }

     if (node.children) {
       for (let i = 0; i < node.children.length; i++) {
         let res = findNode(node.children[i], id);
         if (res) {
           return res;
         }
       }
     }

     return false;
   };

  $("#search").select2({
      data: searchData,
      containerCssClass: "search"
    });

    // attach search box listener
    $("#search").on("select2:select", function(e) {
      // find node with name
      // let n = findNode(nodes, e.params.data.text);
      // console.log(n);
  		// if (n) {
      //   alert(e.params.data.text + " not found!");
  		// }
  		// else {
  		// 	alert(e.params.data.text + " not found!");
  		// }
  	});

}
