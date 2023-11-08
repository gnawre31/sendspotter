import { create } from "zustand";
// import test from "./test.json";

import axios from "axios";

export const useShoeStore = create((set) => ({
  shoes: [],
  loading: false,
  currency: "CAD",
  searchValue: "",
  logos: [],
  sortBy: "discount",
  setSearch: (searchValue) => set(() => ({ searchValue: searchValue })),
  sortShoes: (sortBy, shoes) => {
    const shoesCopy = { ...shoes };
    if (sortBy === "brand") {
      shoesCopy.data.sort((a, b) => a.brand.localeCompare(b.brand));
    } else if (sortBy === "price") {
      shoesCopy.data.sort((a, b) => a.min_sale_price - b.min_sale_price);
    } else if (sortBy === "discount") {
      shoesCopy.data.sort((a, b) => b.max_discount_pct - a.max_discount_pct);
    }
    set(() => ({
      shoes: shoesCopy,
      sortBy: sortBy,
    }));
  },
  getAllShoes: async () => {
    set(() => ({ loading: true }));

    // API call to get all shoe data
    // let shoes = test;

    const data = await axios.get(
      "https://vk3gs5wzz1.execute-api.us-east-1.amazonaws.com/prod/shoes"
    );

    const shoes = data.data.shoes;
    const logos = data.data.logos;

    // at least 1 shoe on discount
    if (shoes.data.length > 0) {
      // determine max discount and min price
      shoes.data = shoes.data.map((shoe) => {
        // min price retailer
        const min_retailer = shoe.retailers.reduce((prev, curr) =>
          prev.sale_price > curr.sale_price ? curr : prev
        );

        shoe.min_sale_price = min_retailer.sale_price;
        shoe.max_discount_pct = min_retailer.discount_pct;
        shoe.img_url = min_retailer.img_url;
        shoe.price = min_retailer.og_price;
        shoe.id = `${shoe.brand}-${shoe.product_name}-${shoe.gender}`.replace(
          /\s+/g,
          "-"
        );

        return shoe;
      });

      // sort by brand by default
      shoes.data.sort((a, b) => b.max_discount_pct - a.max_discount_pct);
      // const sorted_by_price = shoes.data.sort(
      //   (a, b) => a.min_sale_price - b.min_sale_price
      // );

      set(() => ({ shoes: shoes, logos: logos }));
    }

    set(() => ({ loading: false }));
  },
}));
