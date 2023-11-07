
import Filter from '../components/catalogue/Filter'
import ProductGrid from '../components/catalogue/ProductGrid'
import logo from "../assets/sendspotter_350x75_black.svg"
import { useShoeStore } from '../store'



const Home = () => {

    const currency = useShoeStore(state => state.currency)



    return (
        <div>

            <div className='w-[800px] flex m-auto justify-center items-center flex-col mb-24'>
                <div className='w-full flex mt-8 mb-4 justify-between'>
                    <img src={logo} className='w-48' />
                    <p className='flex justify-center items-center text-gray-500'>Rock climbing shoe sales, updated daily</p>
                </div>
                <Filter />
                <p className='text-sm text-gray-400 w-full mt-4 mb-4'>{`Region: Canada, Currency: ${currency} `}</p>
                <ProductGrid />
            </div>
        </div>

    )
}

export default Home