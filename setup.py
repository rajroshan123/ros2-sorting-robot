from setuptools import find_packages, setup

package_name = 'sorting_robot'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        (
            'share/ament_index/resource_index/packages',
            ['resource/' + package_name],
        ),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='rajroshan--',
    maintainer_email='rajroshan---@todo.todo',
    description='Autonomous Smart Sorting Robot',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'sensor_node = sorting_robot.sensor_node:main',
            'sorting_node = sorting_robot.sorting_node:main',
            'movement_node = sorting_robot.movement_node:main',
        ],
    },
)