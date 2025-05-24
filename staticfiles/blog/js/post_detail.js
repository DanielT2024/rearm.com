
document.addEventListener('DOMContentLoaded', function() {
    // Newsletter form handling
    const newsletterForm = document.getElementById('newsletterForm');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            const responseDiv = document.getElementById('newsletterResponse');
            
            fetch(this.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    responseDiv.innerHTML = '<p style="color: green;">Thanks for subscribing!</p>';
                    newsletterForm.reset();
                } else {
                    let errors = '';
                    for (const key in data.errors) {
                        errors += data.errors[key] + '<br>';
                    }
                    responseDiv.innerHTML = `<p style="color: red;">${errors}</p>`;
                }
            })
            .catch(error => {
                responseDiv.innerHTML = '<p style="color: red;">An error occurred. Please try again.</p>';
            });
        });
    }
    
    // Make images in post content responsive
    document.querySelectorAll('.post-content img').forEach(img => {
        img.style.maxWidth = '100%';
        img.style.height = 'auto';
    });
});
