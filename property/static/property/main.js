document.addEventListener('DOMContentLoaded', function() {

    // Alert Messages Animations
    document.querySelectorAll('.message').forEach(msg => {
        msg.addEventListener('animationend', () => {
            setTimeout(()=> {msg.classList.add('fade-out')}, 5000)
        })
    })

    // Navbar For Mobile Devices
    const hamburger = document.querySelector('#nav-hamburger')
    const hamburgerClose = document.querySelector('#nav-hamburger-close')

    hamburger.onclick = () => {
        hamburger.classList.add('d-none')
        hamburgerClose.classList.remove('d-none')
    }

    hamburgerClose.onclick = () => {
        hamburgerClose.classList.add('d-none')
        hamburger.classList.remove('d-none')
    }


    // NAV BUTTONS For Large Screens
    const navPropertyBtn = document.querySelector('#nav-property')
    navPropertyBtn.onmouseover = () => {
        document.querySelector('#nav-salesperson-dropdown').style.display = 'none';
        const navPropertyDropdown = document.querySelector('#nav-property-dropdown')
        navPropertyDropdown.style.display = 'block';
        navPropertyDropdown.onmouseover = () => {
            navPropertyDropdown.onmouseleave = (event) => {
                event.target.style.display = 'none'
            }
        };
        document.querySelector('nav').onmouseleave = () => {
            navPropertyDropdown.style.display = 'none'
        }
    }
    const navSalespersonBtn = document.querySelector('#nav-salesperson')
    navSalespersonBtn.onmouseover = () => {
        document.querySelector('#nav-property-dropdown').style.display = 'none';
        const navSalespersonDropdown = document.querySelector('#nav-salesperson-dropdown')
        navSalespersonDropdown.style.display = 'block';
        navSalespersonDropdown.onmouseover = () => {
            navSalespersonDropdown.onmouseleave = (event) => {
                event.target.style.display = 'none'
            }
        };
        document.querySelector('nav').onmouseleave = () => {
            navSalespersonDropdown.style.display = 'none'
        }
    }


    const page = document.querySelector('.page-identifier').innerHTML
    if (page == 'index') {index()} 
    else if (page == 'add_property') {add_property()}
    else if (page == 'create user') {create_user()}
    else if (page == 'property') {property()}
    else if (page == 'unit_add') {unit_add()}
    else if (page == 'booking') {booking()}
    else if (page == 'view_booking') {view_booking_and_sale('view_booking')}
    else if (page == 'profile') {profile()}
    else if (page == 'note') {note()}
    else if (page == 'sale') {sale()}
    else if (page == 'view_sale') {view_booking_and_sale('view_sale')}
})


function compare_floor(x, y) {

    const x_floor = parseInt(x.floor);
    const y_floor = parseInt(y.floor);

    let comparison = 0;
    if (x_floor > y_floor) {
        comparison = 1;
    } else if (x_floor < y_floor) {
        comparison = -1;
    }
    return comparison
}

function compare_price(x, y) {

    const x_price = parseInt(x.price);
    const y_price = parseInt(y.price);

    let comparison = 0;
    if (x_price > y_price) {
        comparison = 1;
    } else if (x_price < y_price) {
        comparison = -1;
    }
    return comparison
}

function compare_size(x, y) {

    const x_size = parseInt(x.size);
    const y_size = parseInt(y.size);

    let comparison = 0;
    if (x_size > y_size) {
        comparison = 1;
    } else if (x_size < y_size) {
        comparison = -1;
    }
    return comparison
}

function compare_rooms(x, y) {

    const x_rooms = parseInt(x.rooms);
    const y_rooms = parseInt(y.rooms);

    let comparison = 0;
    if (x_rooms > y_rooms) {
        comparison = 1;
    } else if (x_rooms < y_rooms) {
        comparison = -1;
    }
    return comparison
}

function display_unit(units) {
    document.querySelectorAll('.units').forEach(unit => {unit.remove()})
    document.querySelector('#property_units').classList.add('border-top', 'border-dark')
    units.forEach(unit => {
        const div = document.createElement('a')
        div.setAttribute('href', `/unit/${unit.id}`)
        div.classList.add('d-flex', 'justify-content-lg-between', 'border-bottom', 'border-dark', 'pt-2', 'pb-2', 'units', 'flex-column', 'flex-lg-row')
        div.innerHTML = `<div><strong>${unit.unit_id}</strong> - ${unit.size} sq. ft. - (Floor ${unit.floor}) - ${unit.rooms} Rooms</div><div>$ ${unit.price}</div>`
        document.querySelector('#property_units').appendChild(div)
    })
}


function add_property() {
    document.querySelector('#nav-option-add-property').style.borderLeft = '5px solid #5680e6'
}



function create_user() {
    document.querySelector('#nav-option-create-user').style.borderLeft = '5px solid #5680e6'
}



// sort by time/no. of available (all), filter city
function index() {
    fetch('/api/property/all')
    .then(response => response.json())
    .then(properties => {

        if (properties.message == 'No Property Available') {
            const element = document.createElement('div')
            element.classList.add('border-bottom', 'pb-4', 'pt-3', 'd-flex', 'justify-content-center')
            element.innerHTML = '<span>No Property Available.</span>'
            document.querySelector('#property_list').appendChild(element)
        }

        console.log(properties)
        properties.forEach(property => {
            const link = document.createElement('a')
            link.setAttribute('href', `/property/${property.id}`)
            link.setAttribute('id', `property-${property.id}`)
            document.querySelector('#property_list').appendChild(link)

            const container = document.createElement('div')
            container.classList.add('d-flex', 'justify-content-xl-between', 'border-bottom', 'pb-2', 'pt-2', 'flex-column', 'flex-lg-row')
            container.innerHTML = `<div><span>${property.name}</span> -
            <span>${property.city}</span></div><div><span>Units Available: ${property.available_unit_count}</span>
            <span class="small ml-4">${property.timestamp}</span></div>`
        document.querySelector(`#property-${property.id}`).appendChild(container)
        })
    })
};


function availability_toggle() {
    console.log('toggle')
    availability = document.querySelector('#availability').innerHTML
    id = document.querySelector('#property_id').innerHTML
    csrf = Cookies.get('csrftoken')
    console.log(id)
    fetch('/api/property/availability_toggle', {
        headers : {
            'X-CSRFToken': csrf
        },
        method: 'PUT',
        body: JSON.stringify({
            id : id,
            availability : availability
        })
    })
    .then(response => {
        console.log(response);
        location.reload();
    })
}


function property() {
    if (document.querySelector('#availability').innerHTML === 'True') {

        document.querySelector('#status_available').classList.remove('d-none')
        document.querySelector('#make_booking_btn').onclick = () => {
            document.querySelector('#section_property_units').scrollIntoView({behavior: "smooth"})
        }

        id = document.querySelector('#property_id').innerHTML
        fetch(`/api/property/${id}/units`)
        .then(response => response.json())
        .then(units => {
            console.log(units)
            if (units.length === 0) {
                const e = document.createElement('div')
                e.classList.add('d-flex', 'justify-content-center', 'mt-4')
                e.innerHTML = '<p>No Unit Available.</p>'
                document.querySelector('#property_units').appendChild(e)
            } else {

                // Filtering available units
                const available_units = []
                units.forEach(unit => {
                    if (unit.ultimate_availability === true) {
                        console.log(`${unit.unit_id} is available`)
                        available_units.push(unit)
                    }
                })

                document.querySelector('#sort_price').classList.add('active')
                available_units.sort(compare_price)
                console.log(available_units)
                display_unit(available_units)

                document.querySelector('#sort_price').onclick = () => {
                    document.querySelectorAll('.typical-btn-outline').forEach(btn => {btn.classList.remove('active')})
                    document.querySelector('#sort_price').classList.add('active')
                    available_units.sort(compare_price)
                    display_unit(available_units)
                }

                document.querySelector('#sort_floor').onclick = () => {
                    document.querySelectorAll('.typical-btn-outline').forEach(btn => {btn.classList.remove('active')})
                    document.querySelector('#sort_floor').classList.add('active')
                    available_units.sort(compare_floor)
                    display_unit(available_units)
                }

                document.querySelector('#sort_size').onclick = () => {
                    document.querySelectorAll('.typical-btn-outline').forEach(btn => {btn.classList.remove('active')})
                    document.querySelector('#sort_size').classList.add('active')
                    available_units.sort(compare_size)
                    display_unit(available_units)
                }

                document.querySelector('#sort_rooms').onclick = () => {
                    document.querySelectorAll('.typical-btn-outline').forEach(btn => {btn.classList.remove('active')})
                    document.querySelector('#sort_rooms').classList.add('active')
                    available_units.sort(compare_rooms)
                    display_unit(available_units)

                }
            }
            document.querySelectorAll('.availability_toggle').forEach(btn => {
                btn.onclick = availability_toggle;
            })
        })
    } else if (document.querySelector('#availability').innerHTML === 'False') {
        document.querySelector('#status_unavailable').classList.remove('d-none');
        document.querySelectorAll('.availability_toggle').forEach(btn => {
            btn.onclick = availability_toggle;
        })
    }
}

function unit_add() {

    // Selected Add Unit-by-Unit
    document.querySelector('#unit-by-unit-btn').onclick = (event) => {
        document.querySelector('#floor-by-floor-btn').classList.remove('active');
        event.target.classList.add('active')
        document.querySelector('#floor-by-floor').classList.add('d-none')
        document.querySelector('#unit-by-unit').classList.remove('d-none')
    }
    // Selected Add Floor-by-Floor
    document.querySelector('#floor-by-floor-btn').onclick = (event) => {
        document.querySelector('#unit-by-unit-btn').classList.remove('active');
        event.target.classList.add('active')
        document.querySelector('#unit-by-unit').classList.add('d-none')
        document.querySelector('#floor-by-floor').classList.remove('d-none')

        // Input Floor
        document.querySelector('#floor-by-floor-floor-submit-btn').onclick = () => {
            const floor = document.querySelector('#floor-by-floor-floor')
            if (floor.value === '') {
                alert('Please insert a floor number.')
            } else {
                document.querySelector('#floor-by-floor-unit-container').classList.remove('d-none')
                floor.disabled = true
            }
        }

        // Input Number of Units
        document.querySelector('#floor-by-floor-unit-submit-btn').onclick = () => {

            const unit = document.querySelector('#floor-by-floor-unit')
            if (unit.value === '') {
                alert('Please enter Number of Units.')
            } else {
                document.querySelector('#floor-by-floor-id-container').classList.remove('d-none')
                unit.disabled = true
            }
        }

        // Input Unit ID Start With
        document.querySelector('#floor-by-floor-id-submit-btn').onclick = () => {

            // Check if input has been created before.
            if (document.querySelector('#input-created-status').innerHTML === 'false') {
                const id = document.querySelector('#floor-by-floor-id')
                if (id.value === '') {
                    alert('Please fill in Unit-ID-Start-with.')
                } else {
                    document.querySelector('#floor-by-floor-unit-detail').classList.remove('d-none')
                    id.disabled = true

                    const num_unit = document.querySelector('#floor-by-floor-unit').value

                    for (let i = 1; i <= parseInt(num_unit); i++) {
                        const div = document.createElement('div')
                        div.classList.add('mt-3', 'pt-4', 'pb-4', 'border-bottom', 'border-dark')
                        div.innerHTML = 
                        `
                        <h5 class="d-flex justify-content-center"><strong>${id.value}${i}</strong></h5>
                        <div class="d-flex align-items-baseline mt-5">
                            <p class="col-5">Number of Rooms:</p>
                            <input required type="number" class="form-input" name="rooms-${i}" placeholder="3" min="0">
                        </div>
                        <div class="d-flex align-items-baseline mt-3">
                            <p class="col-5">Number of Bathrooms:</p>
                            <input required type="number" class="form-input" name="bathrooms-${i}" placeholder="2" min="0">
                        </div>
                        <div class="d-flex align-items-baseline mt-3">
                            <p class="col-5">Size (sq. ft.):</p>
                            <input required type="number" class="form-input" name="size-${i}" placeholder="1200" min="1">
                        </div>
                        <div class="d-flex align-items-baseline mt-3">
                            <p class="col-5">With Balcony:</p>
                            <select name="balcony-${i}" class="form-input">
                                <option value="yes">Yes</option>
                                <option value="no">No</option>
                            </select>
                        </div>
                        <div class="d-flex align-items-baseline mt-3">
                            <p class="col-5">Price (US Dollar):</p>
                            <input required type="number" class="form-input" name="price-${i}" min='1' placeholder="880000">
                        </div>
                        `

                        document.querySelector('#floor-by-floor-form').append(div)
                    }

                    // Configure the hidden input
                    document.querySelector('input[type="hidden"][name="floor"]').value =
                    document.querySelector('#floor-by-floor-floor').value;

                    document.querySelector('input[type="hidden"][name="num_unit"]').value =
                    document.querySelector('#floor-by-floor-unit').value;

                    document.querySelector('input[type="hidden"][name="unit_id_starts_with"]').value =
                    document.querySelector('#floor-by-floor-id').value;

                    const description = document.createElement('div')
                    description.classList.add('d-flex', 'align-items-baseline', 'mt-4')
                    description.innerHTML = 
                    `
                    <p class="col-5">Optional Description For All Units:</p>
                    <textarea name="description" class="form-input" style="height: 200px;" rows="5" 
                        placeholder="Notes for the Salespeople.."></textarea>
                    `
                    document.querySelector('#floor-by-floor-form').append(description)

                    const submitBtn = document.createElement('div');
                    submitBtn.classList.add('d-flex', 'justify-content-center', 'mt-4');
                    submitBtn.innerHTML = '<input type="submit" class="btn form-btn" value="Add Units">';

                    document.querySelector('#floor-by-floor-form').append(submitBtn);

                    document.querySelector('#input-created-status').innerHTML = 'true';
                }
            }
        }
    }
}


function booking() {
    document.querySelector('#nav-option-my-bookings').style.borderLeft = '5px solid #5680e6'
}


function view_booking_and_sale(option) {

    document.querySelector('#delete_file_btn').onclick = () => {

        const selectedFilesID = []
        const confirmDeleteBtn = document.querySelector('#confirm-delete-btn')

        // Delete Files
        if (confirmDeleteBtn.classList.contains('d-none')) {

            confirmDeleteBtn.classList.remove('d-none')

            // Initialize
            document.querySelectorAll('.checkbox-not-selected').forEach(item => {
                item.classList.remove('d-none')
            })
            document.querySelectorAll('.checkbox-selected').forEach(item => {
                item.classList.add('d-none')
            })

            // Checkbox being clicked (Inactive to Active)
            document.querySelectorAll('.checkbox-not-selected').forEach(checkbox => {
                checkbox.onclick = (event) => {
                    event.target.parentNode.classList.add('d-none')
                    event.target.parentNode.nextElementSibling.classList.remove('d-none')
                    let selected_file_id = event.target.parentNode.parentNode.id
                    console.log(selected_file_id)
                    selectedFilesID.push(parseInt(selected_file_id))
                    console.log(selectedFilesID)
                }
            })

            // Checkbox being clicked (Active to Inactive)
            document.querySelectorAll('.checkbox-selected').forEach(checkbox => {
                checkbox.onclick = (event) => {
                    event.target.parentNode.classList.add('d-none')
                    event.target.parentNode.previousElementSibling.classList.remove('d-none')
                    let selected_file_id = event.target.parentNode.parentNode.id
                    selectedFilesID.splice(selectedFilesID.indexOf(selected_file_id), 1)
                    console.log(selectedFilesID)
                }
            })

            // Confirm Deleting
            confirmDeleteBtn.onclick = () => {
                console.log(selectedFilesID)

                if (option === 'view_booking') {
                    id = document.querySelector('#booking_id').innerHTML
                    csrf = Cookies.get('csrftoken')
    
                    fetch(`/api/delete_booking_file/${id}`, {
                        headers : {
                            'X-CSRFToken': csrf
                        },
                        method: 'POST',
                        body: JSON.stringify({
                            file_id : selectedFilesID
                        })
                    })
                    .then(response => {
                        console.log(response);
                        location.reload()
                    })
                } else if (option === 'view_sale') {
                    id = document.querySelector('#sale_id').innerHTML
                    csrf = Cookies.get('csrftoken')
    
                    fetch(`/api/delete_sale_file/${id}`, {
                        headers : {
                            'X-CSRFToken': csrf
                        },
                        method: 'POST',
                        body: JSON.stringify({
                            file_id : selectedFilesID
                        })
                    })
                    .then(response => {
                        console.log(response);
                        location.reload()
                    })
                }
            }

        } else {
            confirmDeleteBtn.classList.add('d-none')
            document.querySelectorAll('.checkbox-not-selected').forEach(item => {
                item.classList.add('d-none')
            })
            document.querySelectorAll('.checkbox-selected').forEach(item => {
                item.classList.add('d-none')
            })
        }
    }
}

function profile() {
    document.querySelector('#nav-option-my-profile').style.borderLeft = '5px solid #5680e6';
}

function note() {
    document.querySelector('#nav-option-my-notes').style.borderLeft = '5px solid #5680e6';
}


function sale() {
    document.querySelector('#nav-option-my-sales').style.borderLeft = '5px solid #5680e6';
}