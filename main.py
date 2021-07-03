import io, os, json, requests, urllib.request
from bs4 import BeautifulSoup


def main():
    try:
        os.makedirs('./data')
        os.makedirs('./data/images')
    except:
        pass

    req = requests.get('https://ff.garena.com/weapons/index/en/')

    if req.status_code == 200:
        req_soup = BeautifulSoup(req.text, 'html.parser')
        content = req_soup.find('script', {'id': 'weaponTpml'}).string
        soup = BeautifulSoup(content, 'html.parser')
        weapons = soup.find_all('div', {'class': "m-weapon-wrap"})
        weapons_dicts = []

        for weapon in weapons:
            weapon_name = weapon.span.text
            weapon_image = weapon.find('div', class_='m-weapon-gun').img['src']
            urllib.request.urlretrieve(weapon_image, 'data/images/' + weapon_name + '_cover.png')

            if weapon_name == 'new':
                weapon_name = weapon.find_all('span')[1].text
            
            print('Pegando dados da arma ' + weapon_name)

            weapon_details_type = weapon['class'][0]
            weapon_details_ammunition = weapon.find('span', class_='m-bullet')

            if weapon_details_ammunition is not None:
                weapon_details_ammunition = weapon_details_ammunition.text
            else:
                weapon_details_ammunition = 0

            weapon_details_status = {}
            all_status = weapon.find('ul', class_='m-weapon-data')

            for status in all_status.find_all('li'):
                status_name = status.find('div', class_='txt').text.replace(' ', '_').lower()
                weapon_details_status[status_name] = int(status.find('span', class_='num').text)

            weapon_details_attachables = {}
            all_attachables = weapon.find('ul', class_='m-weapon-config item-list')
            attachables_counter = 1

            for attachable in all_attachables.find_all('a'):
                attachable_name = get_att_name(attachables_counter)
                attachable_img = attachable.find('img')['src']
                weapon_details_attachables[attachable_name.lower()] = attachable_img
                urllib.request.urlretrieve(attachable_img, 'data/images/' + attachable_name + '_' + weapon_name + '_att.png')
                attachables_counter = attachables_counter + 1
            
            weapon_details_description = weapon.find('p', class_='m-weapon-txt').text.strip()

            weapon_details_tags = []
            all_tags = weapon.find('div', class_='m-weapon-label')

            for tag in all_tags.find_all('span'):
                weapon_details_tags.append(tag.text)

            weapon_dict = {
                'name': weapon_name,
                'image': weapon_image,
                'details': {
                    'type': weapon_details_type,
                    'ammunition': weapon_details_ammunition,
                    'status': weapon_details_status,
                    'attachables': weapon_details_attachables,
                    'description': weapon_details_description,
                    'tags': weapon_details_tags
                }
            }

            weapons_dicts.append(weapon_dict)

        with io.open('data/weapons.json', 'w', encoding='utf-8') as json_weapons:
            json_weapons.write(json.dumps(weapons_dicts))
            json_weapons.close()

def get_att_name(counter):
    dict_att = {
        1: 'silencer',
        2: 'muzzle',
        3: 'foregrip',
        4: 'magazine',
        5: 'scope',
        6: 'stock',
    }

    return dict_att.get(counter, '')

main()
