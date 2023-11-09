
import { useShoeStore } from '../../store'
import ProductCard from './ProductCard'

const ProductGrid = () => {

  const shoes = useShoeStore(state => state.shoes)
  const loading = useShoeStore(state => state.loading)
  const searchValue = useShoeStore(state => state.searchValue)

  if (loading) return (
    <div>Loading</div>
  )
  else return (
    <div className='flex flex-wrap gap-6 lg:w-[800px] md:w-[600px] w-[310px]'>


      {shoes.data && shoes.data.map((shoe, idx) => {

        if (shoe.brand.toLowerCase().includes(searchValue.toLowerCase()) || shoe.product_name.toLowerCase().includes(searchValue.toLowerCase()))
          return <ProductCard key={idx} shoe={shoe} />
      })}
    </div>
  )


}
export default ProductGrid