
import { useShoeStore } from '../../store'

const Filter = () => {

    const searchValue = useShoeStore(state => state.searchValue)
    const setSearch = useShoeStore(state => state.setSearch)


    return (
        <div className='w-[800px]'>
            <div className='w-3/5 bg-green-500 h-12 rounded-xl'>
                <form className='w-full h-full'>
                    <input type="text"
                        value={searchValue}
                        onChange={e => setSearch(e.target.value)}
                        className='w-full h-full p-4 border rounded-xl'
                        placeholder='Search...'
                    />
                </form>
            </div>
        </div>

    )
}

export default Filter