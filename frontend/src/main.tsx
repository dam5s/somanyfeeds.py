import {StrictMode} from 'react';
import {createRoot} from 'react-dom/client';
import {App} from './App.tsx';

createRoot(document.getElementById('root')!).render(
    <StrictMode>
        <App apiUrl={'http://localhost:8081'}/>
    </StrictMode>,
);
