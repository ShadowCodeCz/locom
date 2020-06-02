from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 2 - Pre-Alpha',
    'Intended Audience :: Developers',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
    'Operating System :: OS Independent'
]

with open("README.md", "r") as fh:
    long_description = fh.read()

description = "Log Comments"

setup(
    name='locom',
    version='0.3.3',
    packages=find_packages(),
    package_data={
        "locom": ["template/*.html"],
    },
    url='https://github.com/ShadowCodeCz/locom',
    project_urls={
        'Source': 'https://github.com/ShadowCodeCz/locom',
        'Tracker': 'https://github.com/ShadowCodeCz/locom/issues',
    },
    author='ShadowCodeCz',
    author_email='shadow.code.cz@gmail.com',
    description=description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=classifiers,
    keywords='log comments',
    install_requires=['generic-design-patterns', "Pillow"],
    entry_points={
    'console_scripts': [
        'locom=locom:main',
    ],
}
)
