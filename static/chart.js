var a=100;
var b=65;
var c=50;
var d=45;
var xValues = ["Calories", "Carbohydrates", "Proteins", "Fats"];
var yValues = [];
yValues.push(a);
yValues.push(b);
yValues.push(c);
yValues.push(d);
var barColors = ["red", "green","blue","orange"];

new Chart("myChart", {
  type: "horizontalBar",
  data: {
    labels: xValues,
    datasets: [{
      backgroundColor: barColors,
      data: yValues
    }]
  },
  options: {
        legend: {display: false},
    title: {
     
    }
  }
});