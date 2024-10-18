import React, {useState} from "react";
import {Link} from 'react-router-dom';
import axios from 'axios';

const EntryScreen=() => {
    const [plateNumber, serPlateNumber] = useState('');
    const [fee, setFee] = useState(0);
    
    const calculateFee=()=>{
        const hourParked = Math.floor(Math.random()*5)+1;
        setFee(hoursParked*10);
    };

    return (

    );

};

export default EntryScreen
