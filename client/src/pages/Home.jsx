
import Filter from '../components/catalogue/Filter'
import ProductGrid from '../components/catalogue/ProductGrid'
import logo from "../assets/sendspotter_350x75_black.svg"
import { useShoeStore } from '../store'
import { Link } from 'react-router-dom'



const Home = () => {

    const currency = useShoeStore(state => state.currency)

    return (
        <div>

            <div className='lg:w-[800px] md:w-[600px] w-[310px] flex m-auto justify-center items-center flex-col mb-24'>
                <div className='w-full  mt-8 mb-4'>
                    <div className='flex justify-between'>
                        <img src={logo} className='w-48' />
                        <Link to="/about" className='flex items-center pl-4 pr-4 hover:text-blue-500'>About</Link>
                    </div>

                    <p className='text-sm text-gray-400'>Rock climbing shoe sales, updated daily</p>
                    <p className='text-sm text-gray-400'>{`Region: Canada, Currency: ${currency} `}</p>
                </div>
                <Filter />

                <ProductGrid />
            </div>
        </div>

    )
}

export default Home