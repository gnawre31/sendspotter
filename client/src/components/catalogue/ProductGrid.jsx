
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
    <div className='flex flex-wrap gap-4 w-[800px]'>


      {shoes.data && shoes.data.map((shoe, idx) => {
        if (shoe.brand.includes(searchValue.toLowerCase()) || shoe.product_name.includes(searchValue.toLowerCase()))
          return <ProductCard key={idx} shoe={shoe} />
      })}
    </div>
  )


}
export default ProductGrid