from apiclient import ApiClient

client = ApiClient('post', '10.55.48.39','clusters/list','{}', 'admin', 'nut@nix/4U')
print(client.get_info())
