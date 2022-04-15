import pytest
import yaml
import  os,sys
from test_object.calculator import Calculator

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_test_data_cal(data_file = os.path.join(base_dir,r'test_data\test_cal.yml')):
    with open(data_file,'r',encoding='utf-8') as f:
        data = yaml.load(f,Loader=yaml.Loader)
        add_data = []
        div_data = []
        for i in data['add1']:
            add_data.append([n for n in i.values()])
        for i in data['div1']:
            div_data.append([n for n in i.values()])
        return add_data,div_data


@pytest.fixture(scope='class')
def msg():
    print("测试开始")
    yield
    print("测试结束")

@pytest.fixture()
def init():
    print('计算开始')
    cal = Calculator()
    yield cal
    print('计算结束')
    del cal


@pytest.mark.usefixtures('msg')
class TestCal():

    @pytest.mark.run(order = 1)
    @pytest.mark.add_test   #用例标记为add_test
    @pytest.mark.parametrize("a,b,result", get_test_data_cal()[0])
    def test_cal_add(self,a,b,result,init):
        cal = init
        c = cal.add(a,b)
        assert c == result

    @pytest.mark.run(order = 2)
    @pytest.mark.div_test   #用例标记为div_test
    @pytest.mark.parametrize("a,b,result", get_test_data_cal()[1])
    def test_cal_div(self,a,b,result,init):
        try:
            cal = init
            c = cal.div(a,b)
            assert c == result
        except  ZeroDivisionError as e:
            assert False
            print('除数为0，未加判断')






if __name__ == "__main__":
    pytest.main(["-v", "test_calculator.py"])
    # os.system("pytest -m div_test")
    # os.system("allure generate ../report/json  -o ../report/html --clean")

