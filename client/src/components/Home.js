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
import Alert from '@mui/material/Alert';
import Snackbar from '@mui/material/Snackbar';
import Slide from '@mui/material/Slide';

function TransitionRight(props) {
  return <Slide {...props} direction="right" />;
}

export default function HomePage() {

    let valueList=[];
    const [file, setFile] = useState();
    const [outputArray, setoutputArray] = useState([]);
    const [getMessage, setGetMessage] = useState({})
    const [getMessage1, setGetMessage1] = useState({});
    const [List,setList]=useState([]);
    
    const [model, setModel] = useState('');
    const [nextDays, setNextDays] = useState(0);
    const [nextHours, setNextHours] = useState(0);
    const [userID, setUserID] = useState('1');

    const [listDays, setListDays] = useState([]);
    const [listHours, setListHours] = useState([]);


    
    const [action, setAction] = useState('train');

    const [processed, setProcessed] = useState(false);
    const [processing, setProcessing] = useState(false);

    const [predcsv, setpredcsv] = useState("");
    const [outputArray1, setoutputArray1] = useState([]);
    const [List1,setList1]=useState([]);

    


    const fileReader = new FileReader();

    const [state, setOpen] = React.useState({
        open:false
});

  const handleClose = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }

    setOpen({open:false});
  };

    const handleChangeOnModel = (event) => {
        setModel(event.target.value);
      };

      
      const {open} = state;


    const handleOnChange = (e) => {
        setFile(e.target.files[0]);        
    };

    function range(start, end) {
        return Array(end - start + 1).fill().map((_, idx) => start + idx)
    }


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


        setListDays(range(0, 31));
        setListHours(range(0,24));
        
    
      }, [])
    
    useEffect(()=>{
        console.log(listDays)
        console.log(listHours)

    },[listDays])


    // const fun1 = () => {
    //     if (file) {
    //         fileReader.onload = function (event) {
    //             const csvOutput = event.target.result;
    //             // setoutput(csvOutput.split('\n'));
    //             setoutputArray(csvOutput.split('\n'));

    //         };

    //         // setoutputArray(output);
    //         fileReader.readAsText(file)
            
    //     }
        
    // }

    const handleOnSubmit = (e) => {
        e.preventDefault();
        
        // fun1();

        let file1 = file;
        const formData = new FormData();
        formData.append("file", file1);
        formData.append("userID", userID)

        // if(model === 'rnn' || model === 'linearregression'){
        //     axios.post('http://127.0.0.1:5000/data', formData,
        //     {
        //     headers: {
        //         'Content-Type': 'multipart/form-data'
        //     },
        //     body:{
        //         'userID':userID
        //     } 

        //     })
        //     .then(function (response) { 
        //         console.log(response.data);
        //         setoutputArray(response.data.split('\n'))

        //     })
        // }else{
            axios.post('http://127.0.0.1:5000/data', formData,
            {
            headers: {
                'Content-Type': 'multipart/form-data'
            },
            body:{
                'userID':userID
            } 

            })
            .then(function (response) { 
                console.log(response.data);
                setoutputArray(response.data.split('\n'))

            })

        // }
        



        
    };

    const handleChangeAction = (event) => {
        setAction(event.target.value);
      };

    useEffect(() => {
        console.log("output array",outputArray)
        
        outputArray.map((record)=>{
                valueList.push([record.split(',')[0], record.split(',')[1]])
            });
        
            
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
        formData.append("userID", userID)

        if(model === 'autoarima'){

            if(action === 'train'){
                axios.post('http://127.0.0.1:5000/autoarima/train', formData, 
                    {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    },
                    body:{
                        'userID':userID
                    } 
                })
                .then(function (response) { 
                    console.log(response.data);
                    setpredcsv(response.data);
                    setProcessing(false);
                    setProcessed(true);
                    setOpen({open:true});
                })
            }else if(action === 'predict'){
                axios.post('http://127.0.0.1:5000/autoarima/predict', {
                headers: {
                'Content-Type': 'application/json'
                },
                body:{
                    "days": nextDays,
                    "hours":nextHours,
                    "userID": userID
                }
                } )
                .then(function (response) { 
                    console.log(response.data);
                    setpredcsv(response.data);
                    setProcessing(false);
                    setProcessed(true);
                })
            }else{
                axios.post('http://127.0.0.1:5000/autoarima/update', formData, {
                headers: {
                'Content-Type': 'multipart/form-data'
                },
                body:{
                    'userID':userID
                } 
                } )
                .then(function (response) { 
                    console.log(response.data);
                    setpredcsv(response.data);
                    setProcessing(false);
                    setProcessed(true);
                    setOpen({open:true});
                })
            }

            


        }else if(model === 'prophet'){
            if(action ==='train'){
                axios.post('http://127.0.0.1:5000/prophet/train', formData, {
            headers: {
                'Content-Type': 'application/json'
            }
            } )
            .then(function (response) {
                console.log(response.data);
                setpredcsv(response.data);
                setProcessing(false);
                setProcessed(true);
                setOpen({open:true});
            })
            }
            else{
            axios.post('http://127.0.0.1:5000/prophet/predict', {
            headers: {
              'Content-Type': 'application/json'
            },
            body:{
                "days": nextDays,
                "hours":nextHours,
                "userID": userID
            }
            } )
            .then(function (response) {
                console.log(response.data);
                setpredcsv(response.data);
                setProcessing(false);
                setProcessed(true);
                setOpen({open:true});
            })}
        }else if(model === 'rnn'){
            // axios.post('http://127.0.0.1:5000/rnn', formData, {
            // headers: {
            //   'Content-Type': 'multipart/form-data'
            // }
            // } )
            // .then(function (response) {
            //     console.log(response.data);
            //     setpredcsv(response.data);
            //     setProcessing(false);
            //     setProcessed(true);
            // })
            if(action === 'train'){
                axios.post('http://127.0.0.1:5000/rnn/train', formData, 
                    {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    },
                    body:{
                        'userID':userID
                    } 
                })
                .then(function (response) { 
                    console.log(response.data);
                    setpredcsv(response.data);
                    setProcessing(false);
                    setProcessed(true);
                    setOpen({open:true});
                })
            }else if(action === 'predict'){
                axios.post('http://127.0.0.1:5000/rnn/predict', {
                headers: {
                'Content-Type': 'application/json'
                },
                body:{
                    "days": nextDays,
                    "hours":nextHours,
                    "userID": userID
                }
                } )
                .then(function (response) { 
                    console.log(response.data);
                    setpredcsv(response.data);
                    setProcessing(false);
                    setProcessed(true);
                })
            }else{
                axios.post('http://127.0.0.1:5000/rnn/update', formData, {
                headers: {
                'Content-Type': 'multipart/form-data'
                },
                body:{
                    'userID':userID
                } 
                } )
                .then(function (response) { 
                    console.log(response.data);
                    setpredcsv(response.data);
                    setProcessing(false);
                    setProcessed(true);
                    setOpen({open:true});
                })
            }




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

        }else if(model === 'linearregression'){

            if(action === 'train'){
                axios.post('http://127.0.0.1:5000/linearRegression/train', formData, {
                headers: {
                'Content-Type': 'multipart/form-data'
                },
                body:{
                    'userID':userID
                } 
                } )
                .then(function (response) { 
                    console.log(response.data);
                    setpredcsv(response.data);
                    setProcessing(false);
                    setProcessed(true);
                    setOpen({open:true});
                })
            }else if(action === 'predict'){
                axios.post('http://127.0.0.1:5000/linearRegression/predict', {
                headers: {
                'Content-Type': 'application/json'
                },
                body:{
                    "days": nextDays,
                    "hours":nextHours,
                    "userID": userID
                }
                } )
                .then(function (response) { 
                    console.log(response.data);
                    setpredcsv(response.data);
                    setProcessing(false);
                    setProcessed(true);
                })
            }else{
                axios.post('http://127.0.0.1:5000/linearRegression/update', formData, {
                headers: {
                'Content-Type': 'multipart/form-data'
                },
                body:{
                    'userID':userID
                } 
                } )
                .then(function (response) { 
                    console.log(response.data);
                    setpredcsv(response.data);
                    setProcessing(false);
                    setProcessed(true);
                    setOpen({open:true});
                })
            }
            
        }

        
          
    }

    useEffect(() => {
        // const fileReader1 = new FileReader();
        setoutputArray1(predcsv.split('\n'));

        // fileReader1.readAsText(predcsv);
    }, [predcsv]);

    useEffect(() => {
        console.log(List1)
    }, [List1]);



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
            outputArray1.map((record)=>(valueList1.push([record.split(',')[0], record.split(',')[1]])));
            // outputArray1.map((record)=>(valueList1.push([record.split('  ')[0], record.split('  ')[1].split(',')[0]])));
            valueList1.unshift([{ type: 'string', label: 'Time' },{label:'Forecast_rnn',type:'number'}])
            setList1(valueList1);
            console.log("output array1 from flask", outputArray1)
            console.log("value list 1",valueList1)

        }else if(model === 'prophet'){
            outputArray1.map((record)=>(valueList1.push([record.split(',')[0], record.split(',')[1]])));
            // outputArray1.map((record)=>(valueList1.push([record.split('  ')[0], record.split('  ')[1].split(',')[0]])));
            valueList1.unshift([{ type: 'string', label: 'Time' },{label:'Forecast',type:'number'}])
            setList1(valueList1);
            console.log("output array1 from flask", outputArray1)
            console.log("value list 1",valueList1)

        }else if(model === 'mlmodels'){
            outputArray1.map((record)=>(valueList1.push([record.split(',')[0], record.split(',')[2],record.split(',')[5], record.split(',')[6],record.split(',')[7],record.split(',')[8]])));
            // outputArray1.map((record)=>(valueList1.push([record.split('  ')[0], record.split('  ')[1].split(',')[0]])));
            valueList1.unshift([{ type: 'string', label: 'Time' },{label:'Usage',type:'number'},{label:'Forecast_Random_forest',type:'number'},{label:'Forecast_LR',type:'number'},{label:'Forecast_Extreme_gradient_descent',type:'number'},{label:'Forecast_MNB',type:'number'}])
            setList1(valueList1);
            console.log("output array1 from flask", outputArray1)
            console.log("value list 1",valueList1)
        }else if(model === 'linearregression'){
            outputArray1.map((record)=>(valueList1.push([record.split(',')[0], record.split(',')[1]])));
            // outputArray1.map((record)=>(valueList1.push([record.split('  ')[0], record.split('  ')[1].split(',')[0]])));
            valueList1.unshift([{ type: 'string', label: 'Time' },{label:'Forecast',type:'number'}])
            setList1(valueList1);
            console.log("output array1 from flask", outputArray1)
            console.log("value list 1",valueList1)
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

                <div style={{alignItems:'center',justifyContent:'center', width:1000, margin:'0px auto'}}>
                    <Box justify = "center">
                    <FormControl sx={{ m: 1, minWidth: 250 }}>
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
                        <MenuItem value={'linearregression'}>Linear Regression</MenuItem>
                        </Select>
                    </FormControl>
                    

                    <FormControl sx={{ m: 1, minWidth: 120 }}>
                        <InputLabel id="demo-simple-select-label">User ID</InputLabel>
                        <Select
                        labelId="demo-simple-select-label"
                        id="demo-simple-select"
                        value={userID}
                        label="Model"
                        onChange={(event)=>{setUserID(event.target.value)}}
                        >
                        <MenuItem value={'1'}>1</MenuItem>
                        <MenuItem value={'2'}>2</MenuItem>
                        <MenuItem value={'3'}>3</MenuItem>
                        <MenuItem value={'4'}>4</MenuItem>

                        </Select>
                    </FormControl>
                    </Box>



                </div>
                    
                <br/>
                
                {model==='autoarima'?
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
                        <FormControlLabel value="update" control={<Radio />} label="Update" />
                    </RadioGroup>
                    </FormControl>
                    
                    
                    
                    :model==='prophet' || model==='linearregression' || model === 'rnn'?
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
                    </FormControl>:<span></span>
                }

                {action === 'predict' && (model === 'autoarima' || model==='linearregression'|| model === 'rnn' || model === 'prophet')?
                    <div>
                        <br/>
                        <div style={{alignItems:'center',justifyContent:'center', width:150, margin:'0px auto'}}>
                                <Box justify = "center" sx={{margin:'15px auto'}}>
                                <FormControl fullWidth>
                                    <InputLabel id="demo-simple-select-label">Days</InputLabel>
                                    <Select
                                    labelId="demo-simple-select-label"
                                    id="demo-simple-select"
                                    value={nextDays}
                                    label="Model"
                                    onChange={(event)=>{setNextDays(event.target.value)}}
                                    >
                                    
                                    {
                                    listDays.map((row, index)=>(
                                        <MenuItem key={index} value={row}>{row}</MenuItem>
                                    ))}

                                    </Select>
                                </FormControl>
                            </Box>
                            <Box justify = "center" sx={{margin:'15px auto'}}>
                                <FormControl fullWidth>
                                    <InputLabel id="demo-simple-select-label">Hours</InputLabel>
                                    <Select
                                    labelId="demo-simple-select-label"
                                    id="demo-simple-select"
                                    value={nextHours}
                                    label="Model"
                                    onChange={(event)=>{setNextHours(event.target.value)}}
                                    >
                                    {
                                    listHours.map((row)=>(
                                        <MenuItem value={row}>{row}</MenuItem>
                                    ))}
                                    </Select>
                                </FormControl>
                            </Box>

                        </div>


                    </div> :
                    
                    <div>
                        <Input 
                        type='file'
                        id='csvFileInput'
                        onChange={handleOnChange}/>
                        &nbsp;&nbsp;
                        <Button variant="contained"
                        onClick={(e) => {
                            handleOnSubmit(e);
                        }}
                        >Import CSV and Plot</Button>

                    </div>

                }


                {/* {model === 'autoarima'?
                    <div style={{alignItems:'center',justifyContent:'center', width:150, margin:'0px auto'}}>
                    <br/>
                    <FormControl fullWidth>
                        <InputLabel id="demo-simple-select-label">User ID</InputLabel>
                        <Select
                        labelId="demo-simple-select-label"
                        id="demo-simple-select"
                        value={userID}
                        label="Model"
                        onChange={(event)=>{setUserID(event.target.value)}}
                        >
                        <MenuItem value={'1'}>1</MenuItem>
                        <MenuItem value={'2'}>2</MenuItem>
                        <MenuItem value={'3'}>3</MenuItem>
                        <MenuItem value={'3'}>4</MenuItem>
                        </Select>
                    </FormControl>
                    </div>:<span></span>
                } */}
                <br/>
                <Button variant="contained"
                    onClick={(e) => {
                        sendCSV(e);
                    }}
                   >Send File</Button>

                   
      <Snackbar 
      anchorOrigin={{ "vertical" : "top" , "horizontal" : "right" }}
      open={open} 
      autoHideDuration={10000} 
      onClose={handleClose}
      TransitionComponent = {TransitionRight}
      >
        <Alert onClose={handleClose} severity="success" sx={{ width: '100%' }}>
          {
            List1.length!==0?List1[1][0]:""
            // List1[1][0]

          }
        </Alert>
      </Snackbar>
            
        </div>

        
        
        <br/>
        {processing? <div><h1>Processing</h1><HourglassTopIcon/></div>:<span></span>}
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
        
        {action === 'predict' && (model === 'autoarima' || model === 'linearregression' || model === 'rnn' || model === 'prophet') && processed?<div><h1>Predictions</h1></div>:<span></span>}
        
        
        

        <div style={{ alignContent: "center", width: '95%', margin:'auto' }}>
            {action === 'predict' && (model === 'autoarima' || model === 'linearregression' || model === 'rnn' || model === 'prophet') && processed?
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