// blog/static/blog/js/newsletter.js
document.addEventListener('DOMContentLoaded', function() {
    const newsletterForm = document.getElementById('newsletter-form');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            
            fetch(this.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Show success message
                    alert('Subscription successful!');
                    // Close modal
                    document.getElementById('newsletter-modal').style.display = 'none';
                } else {
                    // Show errors
                    alert(data.errors.join('\n'));
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    }
});