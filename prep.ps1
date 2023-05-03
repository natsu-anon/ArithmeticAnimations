rm Arithmetic_Animations.zip
rm Arithmetic_Animations\*
cp .\arithmetic_animations.py Arithmetic_Animations\arithmetic_animations.py
cp .\ui.py Arithmetic_Animations\ui.py
cp .\__init__.py Arithmetic_Animations\__init__.py
zip Arithmetic_Animations Arithmetic_Animations\*
rm .\Arithmetic_Animations\*
echo "Ready!"