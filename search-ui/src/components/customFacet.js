import React from "react";
import { MultiCheckboxFacet } from "@elastic/react-search-ui-views";
import { AGE_ORDER } from "../mappings/age_order";


export function CustomFacetView(props) {
    const { label, options, values, ...rest } = props;

    let sortedValues = [...options];

    if (label === "Age") {
        sortedValues.sort(
            (a, b) =>
                AGE_ORDER.indexOf(a.value) - AGE_ORDER.indexOf(b.value)
        );

        
    } else {
        sortedValues.sort((a, b) =>
            a.value.toLowerCase().localeCompare(b.value.toLowerCase())
        );
    }
    
    return (
        <fieldset className="sui-facet">
            <legend className="sui-facet__title">{label}</legend>
            <MultiCheckboxFacet
                {...rest}
                field={label}
                options={sortedValues}
            />
        </fieldset>
    );
}
