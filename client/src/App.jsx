import { useEffect } from "react"
import { useShoeStore } from "./store"
import { Routes, Route, useLocation } from "react-router-dom"
import Home from "./pages/Home"
import PDP from "./pages/PDP"
// import Nav from "./components/Nav"
import ReactGA from 'react-ga';
import About from "./pages/About"

const App = () => {
  const getAllShoes = useShoeStore(state => state.getAllShoes)

  ReactGA.initialize('G-99PB07TDMW');

  const location = useLocation();
  useEffect(() => {
    ReactGA.pageview(location.pathname + location.search);
  }, [location]);


  useEffect(() => {
    getAllShoes()

  }, [])


  return (
    <div className="font-graphik">
      <Routes>
        <Route path="*" element={<Home />} />
        <Route path="/" element={<Home />} />
        <Route path="/shoe/:id" element={<PDP />} />
        <Route path="/about" element={<About />} />

      </Routes>
    </div>
  )
}

export default App
