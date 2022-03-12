from distutils.core import setup

entry_points = {
        'console_scripts': ['richwx = path.to.module:function_name']
},

setup(name = 'richwx',
      entry_points = entry_points,
     )