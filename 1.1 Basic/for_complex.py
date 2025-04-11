# Create a sample collection
users = {'Ana': 'active', 'Elio': 'inactive', 'Sofia': 'active'}

# Strategy:  Iterate over a copy // ejecuting the loop on a copy of the collection
# This is a common pattern in Python to avoid modifying the collection while iterating over it.
#print(users)
for user, status in users.copy().items():
    if status == 'inactive':
        del users[user]

# Strategy:  Create a new collection // nueva coleccion para los datos activados
active_users = {}
for user, status in users.items():
    if status == 'active':
        active_users[user] = status
        print(user ,'\n')

print('Active users:')
# Print the active users
print(active_users)
