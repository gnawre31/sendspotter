import PropTypes from "prop-types"
import { AiOutlineArrowRight } from "react-icons/ai"
import { useShoeStore } from "../../store"

const RetailerCard = (props) => {
    const { discount_pct, sale_price, og_price, web_url, retailer_id } = props.retailer

    const logos = useShoeStore(state => state.logos)
    const l = logos.retailers.filter(logo => logo.retailer_id === retailer_id)

    let logo_url = ""
    if (l.length > 0) logo_url = l[0].logo_url


    const sale_price_formatted = sale_price.toFixed(2)
    const og_price_formatted = og_price.toFixed(2)

    return (
        // <div className='w-full h-16 mb-2 flex'>
        <a href={web_url} target="_blank" rel="noopener noreferrer" className='w-full h-16 mb-2 flex'>
            <span className='w-16 h-16 bg-red-600 rounded-xl flex'>
                <p className='flex justify-center m-auto text-white'>{`-${discount_pct}%`}</p>
            </span>
            <span className='ml-2 flex flex-col justify-center items-center'>
                <p className="text-red-600">{"$" + sale_price_formatted}</p>
                <p className='line-through text-gray-500 text-sm'>{"$" + og_price_formatted}</p>
            </span>
            <span className='md:ml-12 ml-4 h-16 md:w-28 w-20 flex justify-center items-center'>
                <img src={logo_url} className="h-16 md:w-28 w-20 object-contain" />
            </span>

            <div className='ml-2 flex justify-center items-center text-2xl p-4'><AiOutlineArrowRight /></div>
        </a>
        // </div>
    )
}

export default RetailerCard

RetailerCard.propTypes = {
    retailer: PropTypes.object.isRequired,

}