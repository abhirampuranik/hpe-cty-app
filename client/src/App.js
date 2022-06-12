import logo from './logo.svg';
import './App.css';
// import AppBar from '@mui/material/AppBar';
import MenuAppBar from './components/AppbarHome';
import HomePage from './components/Home';
import Storage from './components/Storage'
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import AppLayout from './components/layout/AppLayout';


function App() {
  return (
    // <div>
    //   <MenuAppBar/>
    //   <header className="App-header">
    //     <HomePage/>
    //   </header>
    // </div>
    <BrowserRouter>
            <Routes>
            <Route path='/' element={<AppLayout />}>
                    <Route index element={<HomePage />} />
                    <Route path='/dashboard' element={<HomePage />} />
                    <Route path='/storage' element={<Storage />} />
                </Route>
            </Routes>
        </BrowserRouter>
  );
}

export default App;
