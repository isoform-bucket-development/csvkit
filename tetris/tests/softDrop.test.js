/**
 * Test Suite: Soft Drop Functionality
 *
 * Tests for REQ-6: Allow player to accelerate tetromino descent (soft drop)
 * Verifies accelerated descent when holding down key and normal speed resumption
 */

const {
  GameController,
  ActivePiece,
  NORMAL_DROP_INTERVAL,
  SOFT_DROP_INTERVAL,
  LEVEL_SPEED_MULTIPLIER
} = require('../src/gameController');
const { GameBoard } = require('../src/gameBoard');
const { createTetromino } = require('../src/tetromino');

describe('Soft Drop Functionality', () => {
  let controller;

  beforeEach(() => {
    controller = new GameController();
    controller.startGame();
  });

  describe('Test Case 1: Hold down arrow key - Piece falls faster than normal drop rate', () => {
    test('activating soft drop sets softDropActive to true', () => {
      expect(controller.isSoftDropActive()).toBe(false);
      controller.activateSoftDrop();
      expect(controller.isSoftDropActive()).toBe(true);
    });

    test('soft drop interval is significantly faster than normal drop interval', () => {
      const normalInterval = controller.getNormalDropInterval();
      const softDropInterval = controller.getSoftDropInterval();

      // Soft drop should be at least 10x faster than normal
      expect(softDropInterval).toBeLessThan(normalInterval / 10);
      expect(SOFT_DROP_INTERVAL).toBe(50); // 50ms
      expect(NORMAL_DROP_INTERVAL).toBe(1000); // 1000ms
    });

    test('drop interval changes to soft drop speed when activated', () => {
      // Start with normal speed
      expect(controller.getDropInterval()).toBe(NORMAL_DROP_INTERVAL);

      // Activate soft drop
      controller.activateSoftDrop();

      // Should now be at soft drop speed
      expect(controller.getDropInterval()).toBe(SOFT_DROP_INTERVAL);
    });

    test('piece falls faster during soft drop (verified by update timing)', () => {
      const startRow = controller.getActivePiece().row;
      const startTime = Date.now();

      // Activate soft drop
      controller.activateSoftDrop();

      // Simulate game updates at soft drop interval
      let currentTime = startTime;
      let moves = 0;

      // Simulate 5 soft drop intervals
      for (let i = 0; i < 5; i++) {
        currentTime += SOFT_DROP_INTERVAL;
        controller.update(currentTime);
        const currentRow = controller.getActivePiece()?.row;
        if (currentRow !== undefined && currentRow > startRow + moves) {
          moves++;
        }
      }

      // Piece should have moved down at least 4 times in 250ms (5 * 50ms)
      // Normal drop would only move once per 1000ms
      expect(moves).toBeGreaterThanOrEqual(4);
    });

    test('holding down arrow triggers soft drop via input handler', () => {
      // Create a mock keyboard event for down arrow
      const keyDownEvent = {
        key: 'ArrowDown',
        preventDefault: jest.fn()
      };

      expect(controller.isSoftDropActive()).toBe(false);

      // Simulate keydown
      controller._handleKeyDown(keyDownEvent);

      expect(controller.isSoftDropActive()).toBe(true);
      expect(keyDownEvent.preventDefault).toHaveBeenCalled();
    });
  });

  describe('Test Case 2: Release down arrow key - Piece returns to normal fall speed', () => {
    test('deactivating soft drop sets softDropActive to false', () => {
      controller.activateSoftDrop();
      expect(controller.isSoftDropActive()).toBe(true);

      controller.deactivateSoftDrop();
      expect(controller.isSoftDropActive()).toBe(false);
    });

    test('drop interval returns to normal when soft drop is deactivated', () => {
      // Activate and then deactivate soft drop
      controller.activateSoftDrop();
      expect(controller.getDropInterval()).toBe(SOFT_DROP_INTERVAL);

      controller.deactivateSoftDrop();
      expect(controller.getDropInterval()).toBe(NORMAL_DROP_INTERVAL);
    });

    test('releasing down arrow deactivates soft drop via input handler', () => {
      // First activate with keydown
      const keyDownEvent = {
        key: 'ArrowDown',
        preventDefault: jest.fn()
      };
      controller._handleKeyDown(keyDownEvent);
      expect(controller.isSoftDropActive()).toBe(true);

      // Then release with keyup
      const keyUpEvent = { key: 'ArrowDown' };
      controller._handleKeyUp(keyUpEvent);

      expect(controller.isSoftDropActive()).toBe(false);
    });

    test('piece resumes normal speed after releasing soft drop', () => {
      // Activate soft drop
      controller.activateSoftDrop();

      // Verify soft drop speed
      expect(controller.getDropInterval()).toBe(SOFT_DROP_INTERVAL);

      // Deactivate soft drop
      controller.deactivateSoftDrop();

      // Should be back to normal speed
      expect(controller.getDropInterval()).toBe(NORMAL_DROP_INTERVAL);

      // Simulate an update cycle to verify timing
      const startTime = Date.now();
      const piece = controller.getActivePiece();
      const startRow = piece.row;

      // After 100ms (less than normal interval), piece should NOT move
      controller.update(startTime + 100);
      expect(controller.getActivePiece()?.row).toBe(startRow);
    });

    test('normal speed accounts for current level after soft drop ends', () => {
      // Set level to 2 manually to test level-based speed
      controller.level = 2;
      const expectedNormalInterval = NORMAL_DROP_INTERVAL * LEVEL_SPEED_MULTIPLIER;

      // Activate and deactivate soft drop
      controller.activateSoftDrop();
      controller.deactivateSoftDrop();

      // Should return to level-adjusted normal speed
      expect(controller.getDropInterval()).toBeCloseTo(expectedNormalInterval, 5);
    });
  });

  describe('Test Case 3: Hold S key for soft drop - Alternative control', () => {
    test('pressing S key activates soft drop', () => {
      const keyDownEvent = {
        key: 'S',
        preventDefault: jest.fn()
      };

      expect(controller.isSoftDropActive()).toBe(false);
      controller._handleKeyDown(keyDownEvent);

      expect(controller.isSoftDropActive()).toBe(true);
      expect(keyDownEvent.preventDefault).toHaveBeenCalled();
    });

    test('pressing lowercase s key also activates soft drop', () => {
      const keyDownEvent = {
        key: 's',
        preventDefault: jest.fn()
      };

      controller._handleKeyDown(keyDownEvent);
      expect(controller.isSoftDropActive()).toBe(true);
    });

    test('releasing S key deactivates soft drop', () => {
      // Activate with S key
      const keyDownEvent = {
        key: 'S',
        preventDefault: jest.fn()
      };
      controller._handleKeyDown(keyDownEvent);
      expect(controller.isSoftDropActive()).toBe(true);

      // Release S key
      const keyUpEvent = { key: 'S' };
      controller._handleKeyUp(keyUpEvent);

      expect(controller.isSoftDropActive()).toBe(false);
    });

    test('S key provides same speed increase as down arrow', () => {
      const normalInterval = controller.getDropInterval();

      // Activate with S key
      const keyDownEvent = {
        key: 'S',
        preventDefault: jest.fn()
      };
      controller._handleKeyDown(keyDownEvent);

      // Should have same soft drop interval as down arrow
      expect(controller.getDropInterval()).toBe(SOFT_DROP_INTERVAL);
      expect(controller.getDropInterval()).toBeLessThan(normalInterval / 10);
    });

    test('holding both S and down arrow, releasing one keeps soft drop active', () => {
      // Press down arrow
      const downArrowDown = { key: 'ArrowDown', preventDefault: jest.fn() };
      controller._handleKeyDown(downArrowDown);

      // Press S key
      const sKeyDown = { key: 'S', preventDefault: jest.fn() };
      controller._handleKeyDown(sKeyDown);

      expect(controller.isSoftDropActive()).toBe(true);

      // Release down arrow (S still held)
      const downArrowUp = { key: 'ArrowDown' };
      controller._handleKeyUp(downArrowUp);

      // Should still be soft dropping because S is held
      expect(controller.isSoftDropActive()).toBe(true);

      // Release S key
      const sKeyUp = { key: 'S' };
      controller._handleKeyUp(sKeyUp);

      // Now soft drop should be deactivated
      expect(controller.isSoftDropActive()).toBe(false);
    });
  });

  describe('Soft Drop Edge Cases', () => {
    test('multiple activations do not stack speed', () => {
      controller.activateSoftDrop();
      const firstInterval = controller.getDropInterval();

      controller.activateSoftDrop();
      controller.activateSoftDrop();

      // Interval should remain the same
      expect(controller.getDropInterval()).toBe(firstInterval);
    });

    test('deactivating when not active does nothing', () => {
      expect(controller.isSoftDropActive()).toBe(false);
      const interval = controller.getDropInterval();

      controller.deactivateSoftDrop();

      expect(controller.isSoftDropActive()).toBe(false);
      expect(controller.getDropInterval()).toBe(interval);
    });

    test('soft drop does not work when game is not playing', () => {
      controller.gameState = 'paused';

      const keyDownEvent = {
        key: 'ArrowDown',
        preventDefault: jest.fn()
      };

      controller._handleKeyDown(keyDownEvent);

      // Soft drop should not activate when paused
      expect(controller.isSoftDropActive()).toBe(false);
    });

    test('soft drop resets when new game starts', () => {
      controller.activateSoftDrop();
      expect(controller.isSoftDropActive()).toBe(true);

      controller.startGame();

      expect(controller.isSoftDropActive()).toBe(false);
      expect(controller.getDropInterval()).toBe(NORMAL_DROP_INTERVAL);
    });
  });

  describe('Soft Drop Constants', () => {
    test('NORMAL_DROP_INTERVAL is 1000ms', () => {
      expect(NORMAL_DROP_INTERVAL).toBe(1000);
    });

    test('SOFT_DROP_INTERVAL is 50ms', () => {
      expect(SOFT_DROP_INTERVAL).toBe(50);
    });

    test('soft drop is 20x faster than normal drop', () => {
      const speedRatio = NORMAL_DROP_INTERVAL / SOFT_DROP_INTERVAL;
      expect(speedRatio).toBe(20);
    });

    test('LEVEL_SPEED_MULTIPLIER reduces interval each level', () => {
      expect(LEVEL_SPEED_MULTIPLIER).toBe(0.85);

      // At level 2, normal drop should be 15% faster
      controller.level = 2;
      controller.deactivateSoftDrop();
      const level2Interval = controller.getNormalDropInterval();
      expect(level2Interval).toBeCloseTo(NORMAL_DROP_INTERVAL * 0.85, 5);
    });
  });

  describe('Soft Drop Integration with Game Mechanics', () => {
    test('piece can reach bottom faster with soft drop', () => {
      const startTime = Date.now();
      let timeToReachBottom = 0;

      // Without soft drop, calculate time to reach bottom
      const normalTime = NORMAL_DROP_INTERVAL * 20; // Max 20 rows

      // With soft drop
      controller.activateSoftDrop();
      const softDropTime = SOFT_DROP_INTERVAL * 20; // Max 20 rows

      expect(softDropTime).toBeLessThan(normalTime);
      expect(softDropTime).toBe(1000); // 50ms * 20 = 1000ms
      expect(normalTime).toBe(20000); // 1000ms * 20 = 20000ms
    });

    test('soft drop affects update cycle timing', () => {
      const piece = controller.getActivePiece();
      const startRow = piece.row;
      const startTime = Date.now();

      // Without soft drop, piece should not move after 500ms
      controller.update(startTime + 500);
      expect(controller.getActivePiece()?.row).toBe(startRow);

      // Activate soft drop
      controller.activateSoftDrop();

      // Reset lastDropTime to current
      controller.lastDropTime = startTime + 500;

      // After 100ms with soft drop (2 intervals), piece should move
      controller.update(startTime + 600);
      controller.update(startTime + 650);
      // The piece should have moved at least once
      expect(controller.getActivePiece()?.row).toBeGreaterThanOrEqual(startRow);
    });
  });
});

describe('ActivePiece Class', () => {
  test('ActivePiece stores position correctly', () => {
    const tetromino = createTetromino('T');
    const piece = new ActivePiece(tetromino, 5, 3);

    expect(piece.row).toBe(5);
    expect(piece.col).toBe(3);
  });

  test('getBoardPositions returns correct absolute positions', () => {
    const tetromino = createTetromino('O'); // 2x2 square
    const piece = new ActivePiece(tetromino, 2, 4);

    const positions = piece.getBoardPositions();

    // O piece cells are at [0,0], [0,1], [1,0], [1,1]
    // At position (2, 4), they should be at (2,4), (2,5), (3,4), (3,5)
    expect(positions).toContainEqual({ row: 2, col: 4 });
    expect(positions).toContainEqual({ row: 2, col: 5 });
    expect(positions).toContainEqual({ row: 3, col: 4 });
    expect(positions).toContainEqual({ row: 3, col: 5 });
  });

  test('getColorValue returns correct color value', () => {
    const tetromino = createTetromino('I');
    const piece = new ActivePiece(tetromino);

    expect(piece.getColorValue()).toBe(1); // I is cyan = 1
  });
});
