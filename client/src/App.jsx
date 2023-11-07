import { useEffect } from "react"
import { useShoeStore } from "./store"
import { BrowserRouter, Routes, Route } from "react-router-dom"
import Home from "./pages/Home"
import PDP from "./pages/PDP"
import Nav from "./components/Nav"

const App = () => {
  const getAllShoes = useShoeStore(state => state.getAllShoes)


  useEffect(() => {
    getAllShoes()

  }, [])


  return (
    <BrowserRouter>
      {/* <Nav /> */}
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/shoe/:id" element={<PDP />} />

      </Routes>
    </BrowserRouter>
  )
}

export default App
