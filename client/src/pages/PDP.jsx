import { useEffect, useState } from "react";
import { useShoeStore } from "../store";
import { Link, useParams } from "react-router-dom";
import RetailerCard from "../components/pdp/RetailerCard";
import { AiOutlineArrowLeft } from "react-icons/ai";
import logo from "../assets/sendspotter_350x75_black.svg";

const PDP = () => {
    const params = useParams();

    const shoes = useShoeStore((state) => state.shoes);
    const currency = useShoeStore((state) => state.currency);

    const [shoe, setShoe] = useState(null);
    const [gender, setGender] = useState(null);
    const [date, setDate] = useState(null);

    const months = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ];

    useEffect(() => {
        if (shoes.data && shoes.data.length > 0) {
            const found = shoes.data.filter((s) => s.id === params.id);

            if (found.length > 0) {
                // set shoe state
                setShoe(found[0]);

                // set gender
                if (found[0].gender === "m") setGender("Men's");
                else if (found[0].gender === "f") setGender("Women's");
                else setGender("Unisex");

                // set date
                const date_vals = found[0].date.split("-");
                const year = date_vals[0];
                const month = months[parseInt(date_vals[1]) - 1];
                let day = date_vals[2];
                if (day[0] === "0") day.replace("0", "");
                const date_str = `${month} ${day}, ${year}`;

                setDate(date_str);
            }
        }
    }, [shoes, params.id]);

    if (shoe) {
        return (
            <div className="h-screen w-screen flex items-center overflow-hidden">
                <div className="h-3/4 w-1/2 flex justify-end">
                    <img
                        src={shoe.img_url}
                        className="h-full m-w-full object-cover bg-cover rounded-tl-3xl rounded-bl-3xl"
                    />
                </div>
                <div className=" w-1/2 h-3/4 capitalize p-8">
                    <Link to="/" className="flex items-center hover:text-blue-500">
                        {" "}
                        <AiOutlineArrowLeft className="mr-2" />
                        <img src={logo} className="w-28 hover:text-blue-500" />
                    </Link>
                    <p className="text-5xl font-bold mt-4">{`${shoe.brand} ${shoe.product_name}`}</p>
                    <p className="text-gray-500 mb-8">{gender}</p>
                    <div className="text-gray-500 mb-8">
                        <p>Currency: {currency}</p>
                        <p>Last Updated: {date}</p>
                    </div>
                    <p className="mb-2 font-bold">{`Discounted on ${shoe.retailers.length
                        } site${shoe.retailers.length > 1 ? "s" : ""}:`}</p>
                    <div className="h-1/2 overflow-scroll hide-scroll">
                        {shoe.retailers.map((retailer, idx) => (
                            <RetailerCard key={idx} retailer={retailer} />
                        ))}
                    </div>
                </div>
            </div>
        );
    }
};

export default PDP;
