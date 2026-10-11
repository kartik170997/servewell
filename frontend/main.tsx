import React from 'react';
import {createRoot} from 'react-dom/client';
import Folio from './Folio';
import '../app/globals.css';
createRoot(document.getElementById('root')!).render(<React.StrictMode><Folio/></React.StrictMode>);
