import unittest
from test.task_step import TaskStep
import pdb


class TestTaskStep(unittest.TestCase):

    def setUp(self):
        self.task_step = TaskStep()
        self.outer_task_step = TaskStep()
        self.step_text = '''買う前に知っておきたい用語</h2>
<h3> 耐水圧</h3>
<p>どれだけの水圧に耐えられるか表している数値です。この記事でご紹介するアウターの多くが10000mmほどですが、これは1cm四方あたり10000mmの水圧に耐えられるということを表しています。</p>
<p>小雨の水圧が300mm程度、大雨の水圧が10000mm程度ですので、10000mmの耐水性があればおおよそ大雨に耐えられるということが分かります。</p>
<h3> 透湿性</h3>
<p>1平方メートルの生地が24時間でどれだけの水分を外に出すかを表した数値です。8000gと表示されていれば、一日で8000gの水分を外に出してくれるということです。</p>
<p>数値が高ければ高いほど、蒸れたりベタついたりしにくくなります。</p>
<h3> DWR（Durable Water Repellent）</h3>
<p>DWRを訳すと、耐久撥水加工という意味になります。防水性や透湿性を維持するために、アウターの表面に水分がとどまらないようにする働きがあります。</p>
<h3> ベンチレーションポケット</h3>
<p>アウターの脇の下などに付いているポケットのことで、開けることで湿気を逃がす働きがあります。</p>
'''

    def test_set_headings_from_text(self):
        task_step = self.task_step
        task_step.set_headings_from_text(self.step_text)
        self.assertEqual(task_step.step_text, self.step_text)
        self.assertEqual(task_step.h2, '買う前に知っておきたい用語')
        h3s_expectation = ['耐水圧', '透湿性', 'DWR（Durable Water Repellent）', 'ベンチレーションポケット']
        self.assertEqual(task_step.h3s, h3s_expectation)

    def test_set_step_text(self):
        task_step = self.task_step
        task_step.set_step_text(self.step_text)
        self.assertEqual(task_step.step_text, self.step_text)

if __name__ == '__main__':
    unittest.main()
