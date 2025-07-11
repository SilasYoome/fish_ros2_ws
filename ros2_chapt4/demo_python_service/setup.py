from setuptools import find_packages, setup

package_name = 'demo_python_service'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name+"/resource", ['resource/default.jpg','resource/test1.jpg']),
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
            'learn_face_detect=demo_python_service.learn_face_detect:main',
            'face_detect_node=demo_python_service.face_detect_node:main',
            'face_detect_client_node=demo_python_service.face_detect_client_node:main',
        ],
    },
)
