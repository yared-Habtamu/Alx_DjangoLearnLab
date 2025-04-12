// Enhanced follow functionality with loading states
document.addEventListener('DOMContentLoaded', function() {
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('follow-btn')) {
            e.preventDefault();
            const button = e.target;
            const userId = button.dataset.userId;
            const action = button.dataset.action;
            const url = `/users/${userId}/${action}/`;

            // Set loading state
            const originalText = button.textContent;
            button.disabled = true;
            button.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';

            fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                },
                credentials: 'same-origin'
            })
            .then(response => {
                if (!response.ok) throw new Error('Network response was not ok');
                return response.json();
            })
            .then(data => {
                if (data.error) throw new Error(data.error);

                // Update button state
                const newAction = action === 'follow' ? 'unfollow' : 'follow';
                button.dataset.action = newAction;
                button.innerHTML = newAction === 'follow' ?
                    '<i class="fas fa-user-plus"></i> Follow' :
                    '<i class="fas fa-user-minus"></i> Unfollow';

                // Update follower count if available
                const followerCount = document.querySelector('.follower-count');
                if (followerCount) {
                    const currentCount = parseInt(followerCount.textContent);
                    followerCount.textContent = action === 'follow' ? currentCount + 1 : currentCount - 1;
                }

                // Show success message
                showToast(data.message || `Successfully ${action}ed user`);
            })
            .catch(error => {
                console.error('Error:', error);
                showToast(error.message, 'error');
            })
            .finally(() => {
                button.disabled = false;
            });
        }
    });
});

function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    document.body.appendChild(toast);

    setTimeout(() => {
        toast.classList.add('fade-out');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}