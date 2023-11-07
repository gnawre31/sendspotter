import PropTypes from 'prop-types';
import { Link } from 'react-router-dom';




const ProductCard = (props) => {

    const { id, brand, product_name, max_discount_pct, min_sale_price, price, img_url } = props.shoe

    const price_formatted = price.toFixed(2);
    const min_sale_price_formatted = min_sale_price.toFixed(2);




    return (
        <Link to={`/shoe/${id}`} className='rounded-xl border w-[180px] capitalize'>
            <img src={img_url} className='rounded-tr-xl object-cover rounded-tl-xl h-[180px]' />
            <div className='m-2'>
                <p className='font-bold text-lg'>{brand}</p>
                <p className='text-lg mb-2'>{product_name}</p>
                <div className='flex justify-between'>
                    <span>
                        <p className='text-red-600'>{"$" + min_sale_price_formatted}</p>
                        <p className='line-through text-gray-500 text-sm'>{"$" + price_formatted}</p>
                    </span>
                    <span>
                        <p className='text-white rounded-full bg-red-600 pt-2 pb-2 pl-4 pr-4'>{-max_discount_pct + "%"}</p>
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