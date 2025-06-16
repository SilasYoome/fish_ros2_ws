from setuptools import find_packages, setup

package_name = 'demo_python_package'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='rd400',
    maintainer_email='rd400@todo.todo',
    description='TODO: Package description',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'python_node = demo_python_package.ch01_ros2_python_node:main',
            'person_node = demo_python_package.person_node:main',
            'writer_node = demo_python_package.writter_node:main',
            'learn_thread = demo_python_package.learn_thread:main',
            
        ],
    },
)
