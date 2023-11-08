
import { useShoeStore } from '../../store'

const Filter = () => {

    const searchValue = useShoeStore(state => state.searchValue)
    const setSearch = useShoeStore(state => state.setSearch)
    const sortShoes = useShoeStore(state => state.sortShoes)
    const sortBy = useShoeStore(state => state.sortBy)
    const shoes = useShoeStore(state => state.shoes)


    return (
        <div className='lg:w-[800px] md:w-[600px] w-[310px] flex flex-col'>
            <div className='w-3/5 h-12 rounded-xl mb-2'>
                <form className='w-full h-full'>
                    <input type="text"
                        value={searchValue}
                        onChange={e => setSearch(e.target.value)}
                        className='w-full h-full p-4 border rounded-xl'
                        placeholder='Search...'
                    />
                </form>

            </div>
            <div className="relative mb-2">
                <select
                    id="sort"
                    name="sort"
                    className="block appearance-none h-12 bg-white outline-none text-gray-500 text-sm rounded-xl"
                    onChange={e => sortShoes(e.target.value, shoes)}
                    value={sortBy}
                >
                    <option value="discount" >Sort by biggest discount %</option>
                    <option value="price" >Sort by lowest price $</option>
                    <option value="brand" >Sort by brand name</option>

                </select>
            </div>
        </div>

    )
}

export default Filter