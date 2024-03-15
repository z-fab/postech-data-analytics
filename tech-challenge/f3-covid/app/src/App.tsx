import { BrowserRouter } from "react-router-dom";
import { Router } from "./Router";

export function App() {
   return (
      <BrowserRouter basename="/tc-f3">
         <Router />
      </BrowserRouter>
   );
}
