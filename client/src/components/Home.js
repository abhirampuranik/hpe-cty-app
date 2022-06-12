// import { Home } from '@mui/icons-material';
import React, { useState, useEffect, cloneElement } from 'react';
import Chart from "react-google-charts";
import axios from 'axios'
import Box from '@mui/material/Box';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import { Input, Button  } from '@mui/material';
import HourglassTopIcon from '@mui/icons-material/HourglassTop';
import Radio from "@mui/material/Radio";
import RadioGroup from "@mui/material/RadioGroup";
import FormControlLabel from "@mui/material/FormControlLabel";
import FormLabel from "@mui/material/FormLabel";


export default function HomePage() {

    let valueList=[];
    const [file, setFile] = useState();
    const [outputArray, setoutputArray] = useState([]);
    const [getMessage, setGetMessage] = useState({})
    const [getMessage1, setGetMessage1] = useState({})
    const [List,setList]=useState([]);
    
    const [model, setModel] = useState('');
    
    const [action, setAction] = useState('train');

    const [processed, setProcessed] = useState(false);
    const [processing, setProcessing] = useState(false);

    const [predcsv, setpredcsv] = useState("");
    const [outputArray1, setoutputArray1] = useState([]);
    const [List1,setList1]=useState([]);

    


    const fileReader = new FileReader();


    const handleChangeOnModel = (event) => {
        setModel(event.target.value);
      };

     


    const handleOnChange = (e) => {
        setFile(e.target.files[0]);

        
        // const data = new FormData();

        // data.append('file', e.target.files[0]);
        // data.append('filename', this.fileName.value);

        // fetch('http://localhost:5000/autoarima', {
        // method: 'POST',
        // body: data,
        // }).then((response) => {
        // response.json().then((body) => {
        //     console.log("file went bruh")
        // });
        // });

        
    };

    useEffect(()=>{
        axios.get('http://127.0.0.1:5000/time').then(response => {
          console.log("SUCCESS", response)
          setGetMessage(response)
        }).catch(error => {
          console.log(error)
        })

        axios.get('http://127.0.0.1:5000/hello').then(response => {
          console.log("SUCCESS", response)
          setGetMessage1(response)
        }).catch(error => {
          console.log(error)
        })
        
    
      }, [])



    const fun1 = () => {
        if (file) {
            fileReader.onload = function (event) {
                const csvOutput = event.target.result;
                // setoutput(csvOutput.split('\n'));
                setoutputArray(csvOutput.split('\n'));

            };

            // setoutputArray(output);
            fileReader.readAsText(file)
            
        }
        
    }

    const handleOnSubmit = (e) => {
        e.preventDefault();
        
        fun1();
        
    };

    const handleChangeAction = (event) => {
        setAction(event.target.value);
      };

    useEffect(() => {
        outputArray.map((record)=>(valueList.push([record.split(',')[0], record.split(',')[1]])));
        valueList.unshift([{ type: 'string', label: 'Time' },{label:'Storage Consumption',type:'number'}])
        setList(valueList);
        console.log("List values",valueList)
     }, [outputArray]);


    const sendCSV = (e) => {
        e.preventDefault();
        setProcessing(true);

 
        let file1 = file;
        const formData = new FormData();

        formData.append("file", file1);

        if(model === 'autoarima'){
            axios.post('http://127.0.0.1:5000/autoarima/train', formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
            } )
            .then(function (response) { 
                console.log(response.data);
                setpredcsv(response.data);
                setProcessing(false);
                setProcessed(true);
            })
        }else if(model === 'prophet'){
            axios.post('http://127.0.0.1:5000/prophet', formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
            } )
            .then(function (response) {
                console.log(response.data);
                setpredcsv(response.data);
                setProcessing(false);
                setProcessed(true);
            })
        }else if(model === 'rnn'){
            axios.post('http://127.0.0.1:5000/rnn', formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
            } )
            .then(function (response) {
                console.log(response.data);
                setpredcsv(response.data);
                setProcessing(false);
                setProcessed(true);
            })
        }else if(model === 'mlmodels'){
            axios.post('http://127.0.0.1:5000/mlmodels', formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
            } )
            .then(function (response) {
                console.log(response.data);
                setpredcsv(response.data);
                setProcessing(false);
                setProcessed(true);
            })

        }else{

        }

        
          
    }

    useEffect(() => {
        // const fileReader1 = new FileReader();
        setoutputArray1(predcsv.split('\n'));

        // fileReader1.readAsText(predcsv);
    }, [predcsv]);



    useEffect(() => {
        let valueList1 = []


        if(model === 'autoarima'){
            outputArray1.map((record)=>(valueList1.push([record.split(',')[0], record.split(',')[1]])));
            // outputArray1.map((record)=>(valueList1.push([record.split('  ')[0], record.split('  ')[1].split(',')[0]])));
            valueList1.unshift([{ type: 'string', label: 'Time' },{label:'Forecast',type:'number'}])
            setList1(valueList1);
            console.log("output array1 from flask", outputArray1)
            console.log("value list 1",valueList1)

        }else if(model === 'rnn'){
            outputArray1.map((record)=>(valueList1.push([record.split(',')[0], record.split(',')[1], record.split(',')[2], record.split(',')[3]])));
            // outputArray1.map((record)=>(valueList1.push([record.split('  ')[0], record.split('  ')[1].split(',')[0]])));
            valueList1.unshift([{ type: 'string', label: 'Time' },{label:'Usage',type:'number'},{label:'Forecast_rnn',type:'number'},{label:'Forecast_lstm',type:'number'}])
            setList1(valueList1);
            console.log("output array1 from flask", outputArray1)
            console.log("value list 1",valueList1)

        }else if(model === 'prophet'){


        }else if(model === 'mlmodels'){
            outputArray1.map((record)=>(valueList1.push([record.split(',')[0], record.split(',')[2],record.split(',')[5], record.split(',')[6],record.split(',')[7],record.split(',')[8]])));
            // outputArray1.map((record)=>(valueList1.push([record.split('  ')[0], record.split('  ')[1].split(',')[0]])));
            valueList1.unshift([{ type: 'string', label: 'Time' },{label:'Usage',type:'number'},{label:'Forecast_Random_forest',type:'number'},{label:'Forecast_LR',type:'number'},{label:'Forecast_Extreme_gradient_descent',type:'number'},{label:'Forecast_MNB',type:'number'}])
            setList1(valueList1);
            console.log("output array1 from flask", outputArray1)
            console.log("value list 1",valueList1)
        }else{

        }
        
        
    }, [outputArray1]);
    

    return (
        <div style={{ textAlign: "center", alignContent:"center", alignItems:"center" }}>
          

        <div style={{ textAlign: "center" , alignContent:'center'}}>
            <h1>Upload your data</h1>
            
            <div>{getMessage1.status === 200 ? 
                <h3>{getMessage1.data.message}</h3>
                :
                <h3>LOADING</h3>}
            </div>


            

            <form>

                <Input 
                    type='file'
                    id='csvFileInput'
                    onChange={handleOnChange}

                />
                &nbsp;&nbsp;
                <Button variant="contained"
                    onClick={(e) => {
                        handleOnSubmit(e);
                    }}
                    >Import CSV and Plot</Button>



                &nbsp;
               

                <br/>
                <br/>

                
                <div style={{alignItems:'center',justifyContent:'center', width:250, margin:'0px auto'}}>
                    <Box justify = "center">
                    <FormControl fullWidth>
                        <InputLabel id="demo-simple-select-label">Select Model</InputLabel>
                        <Select
                        labelId="demo-simple-select-label"
                        id="demo-simple-select"
                        value={model}
                        label="Model"
                        onChange={handleChangeOnModel}
                        >
                        <MenuItem value={'autoarima'}>AutoArima</MenuItem>
                        <MenuItem value={'prophet'}>Prophet</MenuItem>
                        <MenuItem value={'rnn'}>RNN</MenuItem>
                        <MenuItem value={'mlmodels'}>ML Models</MenuItem>
                        </Select>
                    </FormControl>
                    </Box>
                </div>
                    
                <br/>
                

                <FormControl>
                    <FormLabel id="demo-row-radio-buttons-group-label">Action</FormLabel>
                    <RadioGroup
                        row
                        aria-labelledby="demo-row-radio-buttons-group-label"
                        name="row-radio-buttons-group"
                        value={action}
                        onChange={handleChangeAction}
                    >
                        <FormControlLabel value="train" control={<Radio />} label="Train" />
                        <FormControlLabel value="predict" control={<Radio />} label="Predict" />

                    </RadioGroup>
                </FormControl>
                
                
                <br/>

                <Button variant="contained"
                    onClick={(e) => {
                        sendCSV(e);
                    }}
                    >Send File</Button>
            </form>
            
        </div>

        
        
        <br/>
        <div style={{ alignContent: "center", width: '95%', margin:'auto'}}>
            {outputArray.length!==0?
                <div>
                <h3>Plot</h3>
                <Chart
                width={'100%'}
                height={'800px'}
                chartType="LineChart"
                loader={<div>Storage consumption Chart</div>}
                data={
                List
                }
                
                options={{
                    chartArea: {                        
                        innerWidth:'80%',
                        width: '70%'
                      },
                hAxis: {
                    title: 'Time',
                },
                backgroundColor: {
                    fill: '#c39ea0',//'#fbf6a7',
                    fillOpacity: 0.8},
                color:"white",
                vAxis: {
                    title: 'Storage consumption (in MB)',
                }
                }}
                /></div>:<span></span>}
        </div>

        <br/>
        {processed?<div><h1>Predictions</h1></div>:<span></span>}
        {processing? <div><h1>Processing</h1><HourglassTopIcon/></div>:<span></span>}
        
        

        <div style={{ alignContent: "center", width: '95%', margin:'auto' }}>
            {processed?
                <Chart
                width={'100%'}
                height={'800px'}
                chartType="LineChart"
                loader={<div>Storage consumption Chart</div>}
                data={
                  List1
                }
                // data={
                //     [["Age", "Weight","pred"], [1,2,2],[3,4,5],[4,3,6],[5,6,8],[7,8,10]]
                // }
                
                options={{
                    chartArea: {                        
                        innerWidth:'90%',
                        width: '70%'
                      },
                hAxis: {
                    title: 'Time',
                },
                backgroundColor: {
                    fill: '#fbf6a7',//'#fbf6a7',#c39ea0
                    fillOpacity: 0.8},
                color:"white",
                vAxis: {
                    title: 'Storage Forecast consumption (in MB)',
                }
                }}
                />:<span></span>}
        </div>
          
        </div>
      );
}