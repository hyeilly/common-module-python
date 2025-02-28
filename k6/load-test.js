import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate, Trend } from 'k6/metrics';

// 사용자 정의 메트릭
const errorRate = new Rate('error_rate');
const requestDuration = new Trend('request_duration');

export const options = {
  // 테스트 시나리오
  scenarios: {
    // 일반적인 부하 테스트
    load_test: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '30s', target: 20 },  // 워밍업: 30초 동안 0->20 사용자
        { duration: '1m', target: 20 },   // 부하 테스트: 1분 동안 20명 유지
        { duration: '30s', target: 50 },  // 스케일업: 30초 동안 20->50 사용자
        { duration: '1m', target: 50 },   // 고부하 테스트: 1분 동안 50명 유지
        { duration: '30s', target: 0 },   // 정상화: 30초 동안 0으로 감소
      ],
    },
  },

  // 테스트 성공/실패 임계값 설정
  thresholds: {
    http_req_duration: ['p(95)<500'],    // 95%의 요청이 500ms 이내 처리
    error_rate: ['rate<0.1'],            // 에러율 10% 미만
    http_req_failed: ['rate<0.05'],      // HTTP 오류 5% 미만
  },
};

// 테스트 실행 함수
export default function () {
  // API 호출 (root 엔드포인트)
  const response = http.get('http://nginx/');
  
  // 응답 시간 기록
  requestDuration.add(response.timings.duration);

  // 응답 검증
  const checkResult = check(response, {
    'status is 200': (r) => r.status === 200,
    'response time OK': (r) => r.timings.duration < 500,
  });

  // 체크 실패 시 에러율 증가
  errorRate.add(!checkResult);

  // 요청 간 랜덤 대기 (1-3초)
  sleep(Math.random() * 2 + 1);
}

// 테스트 시작 전 실행
export function setup() {
  // 초기 연결 테스트
  const checkResponse = http.get('http://nginx/');
  check(checkResponse, {
    'initial connection successful': (r) => r.status === 200,
  });
  console.log('테스트 시작');
}

// 테스트 종료 후 실행
export function teardown(data) {
  console.log('테스트 종료');
} 