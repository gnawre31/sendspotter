import PropTypes from 'prop-types';
import { Link } from 'react-router-dom';




const ProductCard = (props) => {

    const { id, brand, product_name, max_discount_pct, min_sale_price, price, img_url } = props.shoe

    const price_formatted = price.toFixed(2);
    const min_sale_price_formatted = min_sale_price.toFixed(2);




    return (
        <Link to={`/shoe/${id}`} className='rounded-xl border lg:w-[180px] md:w-[160px] w-[140px]'>
            <img src={img_url} className='rounded-tr-xl object-cover rounded-tl-xl lg:h-[180px] md:h-[160px] h-[140px] ' />
            <div className='m-2'>
                <p className='font-bold md:text-lg text-sm capitalize'>{brand}</p>
                <p className='md:text-lg text-sm mb-2'>{product_name}</p>
                <div className='flex justify-between'>
                    <span>
                        <p className='text-red-600 text-sm'>{"$" + min_sale_price_formatted}</p>
                        <p className='line-through text-gray-500 text-sm'>{"$" + price_formatted}</p>
                    </span>
                    <span>
                        <p className='text-white text-sm rounded-full bg-red-600 md:pt-2 md:pb-2 md:pl-4 md:pr-4 pt-1 pb-1 pl-2 pr-2'>{-max_discount_pct + "%"}</p>
                    </span>
                </div>


            </div>


        </Link>
    )
}

ProductCard.propTypes = {
    shoe: PropTypes.object
}

export default ProductCard