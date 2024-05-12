/** @odoo-module **/
import { registry } from "@web/core/registry"; // Import registry from Web
import { useInputField } from "@web/views/fields/input_field_hook"; // Import useInputField hook from Web
const { Component,useRef} = owl; // Import Component and useRef hook from Owl

export class NumberSelectionWidget extends Component {

    static template = 'NumberSelectionWidget'; // Define the template for the component

//    static props = {
//        value: { type: Number, optional: true }, // Define prop for the value of the input
//        placeholder: { type: String, optional: true }, // Define prop for the placeholder of the input
//        name: String, // Define prop for the name attribute of the input
//        min: { type: Number, optional: true }, // Define prop for the minimum value of the input
//        max: { type: Number, optional: true }, // Define prop for the maximum value of the input
//        step: { type: Number, optional: true } // Define prop for the step value of the input
//    };

    constructor() {
        super(...arguments); // Call the parent constructor
        this.inputRef = useRef('input_number'); // Create a reference to the input element
        this.state = { value: this.props.value || 1 }; // Initialize the state with the value prop or 1
    }

    setup(){
        super.setup(); // Call the parent setup method
        this.input = useRef('input_number'); // Create a reference to the input element
        useInputField({ getValue: () => this.props.value || "", refName: "input_number" }); // Use the input field hook
    }

    async onInputValueChange(ev) {
        this.state.value = parseInt(ev.target.value) || 1; // Update the state value when input changes
        console.log(ev.target.value); // Log the input value to console
    }
}

// Extract props from the component attributes
NumberSelectionWidget.extractProps = ({attrs}) => {
    return {
        name: attrs.name,
        inputType: attrs.options.type,
        step: attrs.options.step || 1,
        min: attrs.options.min,
        max: attrs.options.max,
        placeholder: attrs.options.placeholder,
    };
};

registry.category('fields').add('number_selection_widget', NumberSelectionWidget); // Register the component with the registry