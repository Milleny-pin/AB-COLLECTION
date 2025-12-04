function updateQuantity(inputId, delta){
    const input = document.getElementById(inputId);
    let currentValue = parseInt(input.value) || 0;
    let newValue = currentValue + delta;

    if (newValue >=1){
        input.value = newValue;
    }
}