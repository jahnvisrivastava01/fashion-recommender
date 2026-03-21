// Wait for the DOM to fully load
document.addEventListener("DOMContentLoaded", () => {

    // Elements
    const genderRadios = document.querySelectorAll('input[name="gender"]');
    const dressDropdown = document.getElementById("dress");
    const shoesDropdown = document.getElementById("shoes");
    const accessoriesDropdown = document.getElementById("accessories");
    const resultsDiv = document.getElementById("results");
    const getBtn = document.getElementById("getRecommendationsBtn");

    // Update dropdowns when gender is selected
    genderRadios.forEach(radio => {
        radio.addEventListener("change", async () => {
            const gender = document.querySelector('input[name="gender"]:checked').value;
            try {
                const response = await fetch(`http://127.0.0.1:5000/get-options/${gender}`);
                const data = await response.json();

                // Populate dropdowns dynamically
                populateDropdown(dressDropdown, data.Dress || []);
                populateDropdown(shoesDropdown, data.Shoes || []);
                populateDropdown(accessoriesDropdown, data.Accessories || []);

                // Clear previous results
                resultsDiv.innerHTML = "";
            } catch (err) {
                console.error("Error fetching options:", err);
                alert("Failed to fetch options from backend.");
            }
        });
    });

    // Button click to fetch recommendations
    getBtn.addEventListener("click", () => getRecommendations(resultsDiv));
});

// Helper function to populate dropdown
function populateDropdown(dropdown, items) {
    dropdown.innerHTML = `<option value="">--Select--</option>`;
    items.forEach(item => {
        const option = document.createElement("option");
        option.value = item;
        option.textContent = item;
        dropdown.appendChild(option);
    });
}

// Function to fetch and display recommendations
async function getRecommendations(resultsDiv) {
    const gender = document.querySelector('input[name="gender"]:checked')?.value;
    if (!gender) {
        alert("Please select your gender.");
        return;
    }

    // Get selections from dropdowns
    const selections = {
        dress: document.getElementById("dress").value,
        shoes: document.getElementById("shoes").value,
        accessories: document.getElementById("accessories").value
    };

    try {
        const response = await fetch("http://127.0.0.1:5000/recommend", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ gender, selections })
        });

        const data = await response.json();

        if (data.error) {
            throw new Error(data.error);
        }

        // ✅ Display readable results (not [object Object])
        resultsDiv.innerHTML =
            `<h3>Recommended Items:</h3><ul>` +
            data.recommended_items
                .map(r => `<li>${r.item} (Occasions: ${r.occasions.join(", ")})</li>`)
                .join("") +
            `</ul>`;

    } catch (err) {
        console.error("Error fetching recommendations:", err);
        alert("Failed to fetch recommendations. Make sure the backend is running.");
    }
}
