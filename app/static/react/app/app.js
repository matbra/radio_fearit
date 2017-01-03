//<script src="https://unpkg.com/react@15/dist/react.js"></script>
//<script src="https://unpkg.com/react-dom@15/dist/react-dom.js"></script>

import React from 'react';
import ReactDOM from 'react-dom';

var BarChart = require("react-chartjs").Bar;

var MyChart = React.createClass({
    getInitialState : function() {
        return {
            labels : ['bla'],//, 'blub', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'],
            datasets: [
        {
            label: "My First dataset",
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255,99,132,1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1,
            data: [65],//, 59, 80, 81, 56, 55, 40],
        }
    ]
        };
     },
     updateData: function() {
        const datasets = this.state.datasets;
        datasets[0].data = count;
        this.setState({labels: words,
                       datasets: datasets});
     },
     componentDidMount: function() {
    var that = this;
//    document.getElementById("button-show").addEventListener('click', that.updateData, false);
    this.updateData();
  },
    render : function() {
        return <BarChart data={this.state} width="800" height="600"/> // <h1>{words}</h1>; // style={{width: "800px", height: "600px"}}
        }
});

function Welcome(props) {
    return <h1>Hello, {props.name}</h1>;
}

//const element = <Welcome name="Sara" data=data/>;
const element = <MyChart/>;
ReactDOM.render(element, document.getElementById('figure'));