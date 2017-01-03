//<script src="https://unpkg.com/react@15/dist/react.js"></script>
//<script src="https://unpkg.com/react-dom@15/dist/react-dom.js"></script>

import React from 'react';
import ReactDOM from 'react-dom';

function Welcome(props) {
    return <h1>Hello, {props.name}</h1>;
}

const element = <Welcome name="Sara" />;
ReactDOM.render(element, document.getElementById('figure'));