import os

for date_folder in os.listdir('images'):
    year, month, day = date_folder.split('-')
    print(date_folder)
    for sale_folder in os.listdir('images/' + date_folder):

        if not os.path.exists('datasets/' + sale_folder):
            os.makedirs('datasets/' + sale_folder)

        print(date_folder)

        for image in os.listdir('images/' + date_folder + '/' + sale_folder):
            print(image)
            time, extension = image.split('.')
            hour, minute, second = time.split('-')
            os.rename('images/' + date_folder + '/' + sale_folder + '/' + image,
                      'datasets/' + sale_folder + '/' +
                      year + '_' + month + '_' + day + '-' +
                      hour + '_' + minute + '_' + second + '.' + extension)
