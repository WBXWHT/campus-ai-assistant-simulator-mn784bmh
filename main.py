import json
import random
import datetime
from typing import Dict, List, Any

class UserProfile:
    """用户档案类，模拟存储用户历史数据"""
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.study_history = []
        self.preferences = {}
        
    def add_study_record(self, subject: str, duration: int, score: float):
        """添加学习记录"""
        record = {
            "subject": subject,
            "duration": duration,
            "score": score,
            "timestamp": datetime.datetime.now().isoformat()
        }
        self.study_history.append(record)
        
    def set_preferences(self, preferred_subjects: List[str], learning_style: str):
        """设置用户偏好"""
        self.preferences = {
            "preferred_subjects": preferred_subjects,
            "learning_style": learning_style
        }

class MockLLM:
    """模拟大语言模型，生成个性化建议"""
    
    # 模拟的知识库和模板
    SUBJECT_ADVICE = {
        "数学": ["建议每天练习10道典型题目", "重点关注函数与几何章节", "建立错题本记录常见错误"],
        "英语": ["每日背诵20个高频词汇", "多听英语播客提升听力", "每周写一篇英语短文"],
        "编程": ["每天完成一个小项目", "阅读开源代码学习规范", "参与编程社区讨论"]
    }
    
    STYLE_ADVICE = {
        "视觉型": ["使用思维导图整理知识点", "观看相关教学视频", "制作彩色笔记"],
        "听觉型": ["录制知识点反复听", "参加学习小组讨论", "听课程录音复习"],
        "实践型": ["多做实验和练习", "参与项目实践", "动手操作加深理解"]
    }
    
    def generate_advice(self, user_profile: UserProfile) -> Dict[str, Any]:
        """生成个性化学习建议"""
        
        if not user_profile.study_history:
            return self._get_default_advice()
        
        # 分析历史数据
        subject_stats = self._analyze_subjects(user_profile.study_history)
        
        # 生成建议
        advice = {
            "user_id": user_profile.user_id,
            "generated_at": datetime.datetime.now().isoformat(),
            "overview": self._generate_overview(subject_stats),
            "specific_advice": [],
            "weekly_plan": self._generate_weekly_plan(user_profile)
        }
        
        # 添加具体科目建议
        for subject, stats in subject_stats.items():
            subject_advice = {
                "subject": subject,
                "strength": stats["avg_score"] >= 80,
                "suggestions": self._get_subject_suggestions(subject, stats, user_profile.preferences)
            }
            advice["specific_advice"].append(subject_advice)
            
        return advice
    
    def _analyze_subjects(self, history: List[Dict]) -> Dict[str, Dict]:
        """分析各科目学习情况"""
        stats = {}
        for record in history:
            subject = record["subject"]
            if subject not in stats:
                stats[subject] = {"total_duration": 0, "total_score": 0, "count": 0}
            
            stats[subject]["total_duration"] += record["duration"]
            stats[subject]["total_score"] += record["score"]
            stats[subject]["count"] += 1
        
        # 计算平均值
        for subject in stats:
            count = stats[subject]["count"]
            stats[subject]["avg_duration"] = stats[subject]["total_duration"] / count
            stats[subject]["avg_score"] = stats[subject]["total_score"] / count
            
        return stats
    
    def _generate_overview(self, stats: Dict) -> str:
        """生成学习概况总结"""
        if not stats:
            return "暂无学习历史数据，请开始你的学习之旅！"
        
        best_subject = max(stats.items(), key=lambda x: x[1]["avg_score"])
        total_study = sum(s["total_duration"] for s in stats.values())
        
        return f"近期你学习了{len(stats)}门科目，总计学习{total_study}分钟。{best_subject[0]}科目表现最佳，平均分{best_subject[1]['avg_score']:.1f}分。"
    
    def _get_subject_suggestions(self, subject: str, stats: Dict, preferences: Dict) -> List[str]:
        """获取科目具体建议"""
        suggestions = []
        
        # 基于科目类型的建议
        if subject in self.SUBJECT_ADVICE:
            suggestions.extend(random.sample(self.SUBJECT_ADVICE[subject], 2))
        
        # 基于学习风格的建议
        learning_style = preferences.get("learning_style", "")
        if learning_style in self.STYLE_ADVICE:
            suggestions.append(random.choice(self.STYLE_ADVICE[learning_style]))
        
        # 基于成绩的建议
        if stats["avg_score"] < 70:
            suggestions.append(f"当前平均分{stats['avg_score']:.1f}，建议加强基础练习")
        elif stats["avg_score"] > 90:
            suggestions.append(f"当前平均分{stats['avg_score']:.1f}，可以挑战更高难度内容")
        
        return suggestions
    
    def _generate_weekly_plan(self, user_profile: UserProfile) -> List[Dict]:
        """生成周学习计划"""
        plan = []
        days = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
        
        preferred = user_profile.preferences.get("preferred_subjects", ["数学", "英语"])
        
        for i, day in enumerate(days):
            subject = preferred[i % len(preferred)]
            plan.append({
                "day": day,
                "subject": subject,
                "task": f"学习{subject} {random.randint(30, 90)}分钟",
                "focus": random.choice(["基础知识", "难点突破", "综合练习"])
            })
        
        return plan
    
    def _get_default_advice(self) -> Dict[str, Any]:
        """获取默认建议（无历史数据时）"""
        return {
            "overview": "欢迎使用校园AI助手！请先开始学习以获取个性化建议。",
            "suggestions": ["从你感兴趣的科目开始学习", "设定每日学习目标", "定期复习巩固知识"],
            "weekly_plan": []
        }

def main():
    """主函数：模拟校园AI助手核心功能"""
    print("=== 校园AI助手 - 个性化学习建议生成器 ===\n")
    
    # 创建模拟用户
    user = UserProfile("student_001")
    user.set_preferences(["数学", "英语", "编程"], "视觉型")
    
    # 添加模拟学习记录
    user.add_study_record("数学", 120, 85.5)
    user.add_study_record("英语", 90, 78.0)
    user.add_study_record("数学", 60, 92.0)
    user.add_study_record("编程", 180, 88.5)
    user.add_study_record("英语", 120, 82.0)
    
    # 初始化模拟大模型
    llm = MockLLM()
    
    # 生成个性化建议
    print("正在分析你的学习数据...")
    advice = llm.generate_advice(user)
    
    # 输出结果
    print(f"\n📊 学习概况：{advice['overview']}")
    print(f"\n🎯 个性化建议：")
    
    for item in advice["specific_advice"]:
        strength = "优势科目" if item["strength"] else "需加强科目"
        print(f"\n  📚 {item['subject']} ({strength})：")
        for suggestion in item["suggestions"]:
            print(f"    • {suggestion}")
    
    print(f"\n📅 本周学习计划：")
    for day_plan in advice["weekly_plan"]:
        print(f"  {day_plan['day']}: {day_plan['task']} ({day_plan['focus']})")
    
    print(f"\n⏰ 生成时间：{advice['generated_at']}")
    print("\n=== 分析完成 ===")
    
    # 模拟A/B测试结果展示
    print("\n📈 模拟A/B测试结果（上线后效果）：")
    print("  • 目标页面用户停留时长提升：35%")
    print("  • 次日留存率提升：18%")

if __name__ == "__main__":
    main()