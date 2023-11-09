import React from 'react'

import logo from "../assets/sendspotter_350x75_black.svg"
import { useShoeStore } from '../store'
import { Link } from 'react-router-dom'


const About = () => {

    const logos = useShoeStore(state => state.logos)
    console.log(logos)
    return (
        <div className='w-screen h-screen mb-12'>
            <span className='md:w-[450px] w-[300px] flex justify-center m-auto flex-col mt-12 text-sm md:text-base '>
                <Link to="/">
                    <img src={logo} className='w-48 flex justify-center m-auto mb-8' />
                </Link>
                <p className='md:text-3xl text-md font-bold flex justify-center mb-2'>Never miss a shoe sale!</p>
                <p className='mb-2'>We gather discounts on climbing shoes from popular retailers so you can stay up to date with them sweet deals.</p>
                <p className='mb-4'>Have an idea? Share how SendSpotter could improve through an anonymous <a href='https://forms.gle/AVd3bdZXV1YHBd8t5' target="_blank" rel="noopener noreferrer" className='text-blue-500'>Google Form</a> or shoot us an email at sendspotter@gmail.com!</p>
                <p>Canadian Sites tracked:</p>
                <span className='text-blue-500 flex flex-col mb-8'>
                    <a href='https://www.mec.ca/en'>https://www.mec.ca/en</a>
                    <a href='https://vpo.ca'>https://vpo.ca</a>
                    <a href='https://climbonequipment.com'>https://climbonequipment.com</a>
                    <a href='https://www.sail.ca/en/'>https://www.sail.ca/en/</a>
                    <a href='https://www.altitude-sports.com'>https://www.altitude-sports.com</a>
                    <a href='https://www.thelasthunt.com'>https://www.thelasthunt.com</a>
                    <a href='https://www.madrock.ca'>https://www.madrock.ca</a>
                    <a href='https://www.vertical-addiction.com/us/'>https://www.vertical-addiction.com/us/</a>
                </span>
                <p>US Sites tracked:</p>
                <p className='italic'>Coming Soon!</p>

            </span>


        </div>
    )
}

export default About